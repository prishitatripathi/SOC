from typing import Any, Dict, List

def call_model(prompt: str, context: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Local stub that simulates an LLM call by echoing prompt + context."""
    ctx_text = "\n".join([c.get("text", "") for c in (context or [])])
    text = f"MODEL_RESPONSE:\nPrompt:\n{prompt}\nContext:\n{ctx_text}"
    return {"text": text, "metadata": {"model": "local-stub"}}
