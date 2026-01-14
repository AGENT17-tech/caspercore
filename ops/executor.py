from ops.commands import commands



def execute(intent_packet: dict):
    intent = intent_packet.get("intent")
    context = intent_packet.get("context", {})

    try:
        result = commands[intent](context)
    except Exception as e:
        return {
            "speech": f"An error occurred: {e}",
            "needs_confirm": False
        }

    # Normalize result (HARDENED)
    if isinstance(result, str):
        return {
            "speech": result,
            "needs_confirm": False
        }

    if isinstance(result, dict):
        return result

    return {
        "speech": "I encountered an unexpected response.",
        "needs_confirm": False
    }
