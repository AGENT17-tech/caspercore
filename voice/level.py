import sounddevice as sd
import numpy as np

LEVEL = 0.0
_stream = None  # keep reference

def start_level_monitor():
    global _stream

    def callback(indata, frames, time, status):
        global LEVEL
        LEVEL = float(np.linalg.norm(indata)) / max(frames, 1)

    _stream = sd.InputStream(
        callback=callback,
        channels=1,
        samplerate=16000
    )
    _stream.start()
