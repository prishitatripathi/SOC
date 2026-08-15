import json
from typing import List, Dict
import os

_sources = []
_loaded = False

def _load_sources():
    global _loaded, _sources
    if _loaded:
        return
    path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "rag_sources.json")
    path = os.path.normpath(path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            _sources = json.load(f)
    except Exception:
        _sources = []
    _loaded = True

def query_rag(query_text: str, top_k: int = 3) -> List[Dict[str, str]]:
    """Naive keyword-based RAG lookup over `data/rag_sources.json`."""
    _load_sources()
    q = query_text.lower()
    scored = []
    for s in _sources:
        score = 0
        content = (s.get("content") or "").lower()
        for tok in q.split():
            if tok in content:
                score += 1
        if score > 0:
            scored.append({"source_id": s.get("source_id"), "text": s.get("content"), "score": float(score)})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
