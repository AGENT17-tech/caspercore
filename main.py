from brain.states import State
from brain.brain import process
from voice.stt import listen
from voice.tts import speak
from brain.states import set_state, State
state = State.IDLE

def log(s): print(f"[STATE] {s}")

while True:
    set_state(State.LISTENING)
    text = listen()

    set_state(State.PROCESSING)
    response = process(text)

    set_state(State.SPEAKING)
    speak(response)

    set_state(State.IDLE)
