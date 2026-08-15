def check_guardrail(text: str) -> dict:
    """Very small example guardrail: flag if text contains 'forbidden' or 'danger'."""
    lowered = text.lower()
    if "forbidden" in lowered or "danger" in lowered:
        return {"caught": True, "reason": "contains forbidden/danger keyword", "details": {}}
    return {"caught": False, "reason": "", "details": {}}
