from brain.states import State
from brain.brain import process
from voice.stt import listen
from voice.tts import speak

state = State.IDLE

def log(s): print(f"[STATE] {s}")

while True:
    state = State.LISTENING
    log(state)

    text = listen()
    print(f"[YOU] {text}")

    state = State.PROCESSING
    log(state)

    response = process(text)

    state = State.SPEAKING
    log(state)
    speak(response)

    state = State.IDLE
    log(state)
