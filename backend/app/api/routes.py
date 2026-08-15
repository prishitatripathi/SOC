from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List
from ..db.session import get_session, create_db_and_tables
from ..models.schemas import Payload, Result
from ..attack.engine import inject
from ..guardrail.guard import check_guardrail
from ..rag.vectorstore import query_rag
from ..llm.adapter import call_model
from ..eval.runner import validate_output
from sqlmodel import Session
import uuid, datetime, json

router = APIRouter()


@router.on_event("startup")
def on_startup():
    create_db_and_tables()


@router.post("/run-evaluation")
def run_evaluation(guardrail: str = "on", repeat: int = 1, session: Session = Depends(get_session)):
    run_id = str(uuid.uuid4())
    started_at = datetime.datetime.utcnow().isoformat()
    payloads: List[Payload] = session.exec(select(Payload)).all()
    results = []
    for _ in range(max(1, repeat)):
        for p in payloads:
            injected = inject(p.content)
            guard = None
            if guardrail == "on":
                guard = check_guardrail(injected)
                if guard.get("caught"):
                    outcome = "caught"
                    llm_resp = {"text": "", "metadata": {}}
                    validator = {"status": "caught", "evidence": ["guardrail caught"], "confidence": 1.0}
                    result = Result(result_id=str(uuid.uuid4()), run_id=run_id, payload_id=p.id, outcome=outcome,
                                    guardrail_json=json.dumps(guard), llm_response_json=json.dumps(llm_resp),
                                    validator_json=json.dumps(validator),
                                    timestamps_json=json.dumps({"started_at": started_at, "finished_at": datetime.datetime.utcnow().isoformat()}))
                    session.add(result); session.commit(); session.refresh(result)
                    results.append(result)
                    continue

            context = query_rag(injected)
            llm_out = call_model(injected, context)
            validator = validate_output(llm_out)
            outcome = validator.get("status", "partial")
            result = Result(result_id=str(uuid.uuid4()), run_id=run_id, payload_id=p.id, outcome=outcome,
                            guardrail_json=json.dumps(guard or {}), llm_response_json=json.dumps(llm_out),
                            validator_json=json.dumps(validator),
                            timestamps_json=json.dumps({"started_at": started_at, "finished_at": datetime.datetime.utcnow().isoformat()}))
            session.add(result); session.commit(); session.refresh(result)
            results.append(result)

    # Build simple summary
    counts = {"succeeded": 0, "caught": 0, "partial": 0, "total": len(results)}
    for r in results:
        if r.outcome == "succeeded":
            counts["succeeded"] += 1
        elif r.outcome == "caught":
            counts["caught"] += 1
        else:
            counts["partial"] += 1

    return {"run_id": run_id, "counts": counts, "results_preview": [{"result_id": r.result_id, "payload_id": r.payload_id, "outcome": r.outcome} for r in results]}


@router.get("/replay/{result_id}")
def replay(result_id: str, session: Session = Depends(get_session)):
    statement = select(Result).where(Result.result_id == result_id)
    res = session.exec(statement).one_or_none()
    if not res:
        return {"error": "not found"}
    return {"result_id": res.result_id, "payload_id": res.payload_id, "guardrail": json.loads(res.guardrail_json or "{}"), "llm_response": json.loads(res.llm_response_json or "{}"), "validator": json.loads(res.validator_json or "{}")}
