def process(text: str) -> str:
    text = text.lower()

    if "status" in text:
        return "All systems operational."

    if "time" in text:
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%H:%M')}."

    return "Command received."
