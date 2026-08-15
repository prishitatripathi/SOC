def inject(payload_text: str) -> str:
    """Create a log-entry style message to send to the target model."""
    return f"[LOG ENTRY] {payload_text}"
