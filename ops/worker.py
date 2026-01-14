from PySide6.QtCore import QObject, Signal
import threading

from ops.router import detect_intent
from ops.executor import execute


class OperatorWorker(QObject):
    result = Signal(dict)
    state = Signal(str)

    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        self._text = None

    def handle_text(self, text: str):
        with self._lock:
            self._text = text

        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        with self._lock:
            text = self._text

        if not text:
            return

        # Processing state
        self.state.emit("PROCESSING")

        # Detect intent
        intent_packet = detect_intent(text)

        # Execute command
        response = execute(intent_packet)

        # Emit result
        self.result.emit(response)
