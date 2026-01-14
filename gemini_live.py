import asyncio
import base64
import threading
from google import genai
import pyaudio

MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"

FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

CONFIG = {
    "response_modalities": ["AUDIO"],  # get audio back
    "system_instruction": "You are Casper. Calm, precise, helpful.",
}

class GeminiLiveAudio:
    def __init__(self, on_event):
        """
        on_event: callable(event_type: str, payload: dict)
          event_type examples: "assistant_audio", "assistant_text", "transcript"
        """
        self.on_event = on_event
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def start_in_thread(self):
        threading.Thread(target=lambda: asyncio.run(self._run()), daemon=True).start()

    async def _run(self):
        client = genai.Client()  # uses GOOGLE_API_KEY env var

        pya = pyaudio.PyAudio()
        mic = pya.open(format=FORMAT, channels=CHANNELS, rate=SEND_SAMPLE_RATE,
                       input=True, frames_per_buffer=CHUNK_SIZE)
        spk = pya.open(format=FORMAT, channels=CHANNELS, rate=RECEIVE_SAMPLE_RATE,
                       output=True, frames_per_buffer=CHUNK_SIZE)

        async with client.aio.live.connect(model=MODEL, config=CONFIG) as session:
            # two tasks: send mic, receive audio
            send_task = asyncio.create_task(self._send_mic(session, mic))
            recv_task = asyncio.create_task(self._recv(session, spk))
            await asyncio.wait([send_task, recv_task], return_when=asyncio.FIRST_EXCEPTION)

    async def _send_mic(self, session, mic):
        while not self._stop.is_set():
            data = mic.read(CHUNK_SIZE, exception_on_overflow=False)
            # Live API expects PCM chunks in realtimeInput
            await session.send_audio(data)

    async def _recv(self, session, spk):
        async for event in session.receive():
            # SDK event shapes vary; you’ll map them once you print them.
            # Typical: audio chunks + optional transcripts/tool calls
            if event.type == "audio":
                spk.write(event.data)
                self.on_event("assistant_audio", {})
            elif event.type == "text":
                self.on_event("assistant_text", {"text": event.text})
            elif event.type == "transcript":
                self.on_event("transcript", {"text": event.text})
