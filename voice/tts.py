import pyttsx3
import queue
import threading

_engine = pyttsx3.init(driverName="espeak")
_engine.setProperty("rate", 155)
_engine.setProperty("volume", 1.0)

_q = queue.Queue()
_running = False


def _worker():
    global _running
    while True:
        text = _q.get()
        if text is None:
            break
        _engine.say(text)
        _engine.runAndWait()
        _q.task_done()
    _running = False


def speak(text: str):
    global _running
    if not text:
        return
    _q.put(text)
    if not _running:
        _running = True
        threading.Thread(target=_worker, daemon=True).start()
