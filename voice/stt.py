import whisper
from voice.audio import record
from core.events import emit
# FORCE CPU — NO CUDA
model = whisper.load_model("base", device="cpu")

def listen():
    record()
    print("[STT] Transcribing (CPU)...")
    result = model.transcribe(
        "record.wav",
        fp16=False,          # critical
        language="en"
    )
    text = result["text"].strip()
    emit("transcript", text)
    return text
