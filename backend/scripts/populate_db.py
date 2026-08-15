"""Populate the local SQLite DB with example payloads and RAG sources."""
import json
import os
from sqlmodel import Session
from backend.app.db.session import engine, create_db_and_tables
from backend.app.models.schemas import Payload, RagSource


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
DATA_DIR = os.path.normpath(DATA_DIR)


def load_json(name):
    path = os.path.join(os.path.dirname(__file__), "..", "..", "data", name)
    path = os.path.normpath(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    create_db_and_tables()
    payloads = load_json("payloads.json")
    rag = load_json("rag_sources.json")
    with Session(engine) as session:
        # insert payloads
        for p in payloads:
            session.add(Payload(category=p.get("category"), content=p.get("content"), tags=p.get("tags")))
        # insert rag sources
        for s in rag:
            session.add(RagSource(source_id=s.get("source_id"), title=s.get("title"), content=s.get("content"), metadata=s.get("metadata")))
        session.commit()

    print("Database populated at", engine.url)


if __name__ == "__main__":
    main()
