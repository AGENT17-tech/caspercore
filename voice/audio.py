from email.mime import audio
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

RATE = 16000
DURATION = 5  # seconds

def record(filename="record.wav"):
    print("[AUDIO] Recording...")
    audio = sd.rec(int(DURATION * RATE), samplerate=RATE, channels=1, dtype=np.int16)
    sd.wait()
    write(filename, RATE, audio)
    print("[AUDIO] Saved.")

def play(audio_data, sample_rate=16000):
    print("[AUDIO] Playing...")
    sd.play(audio_data, samplerate=sample_rate)
    sd.wait()
    print("[AUDIO] Done.")
    print(f"[AUDIO] Max amplitude: {audio.max()}")
