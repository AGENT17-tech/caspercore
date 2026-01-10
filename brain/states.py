from core.events import emit

class State:
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    PROCESSING = "PROCESSING"
    SPEAKING = "SPEAKING"

def set_state(state):
    emit("state", state)
