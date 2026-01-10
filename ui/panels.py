from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from ui.theme import TEXT, CYAN
from core.events import subscribe

class LeftPanel(QWidget):
    def __init__(self):
        super().__init__()
        l = QVBoxLayout(self)
        self.label = QLabel("TRANSCRIPTS\n—")
        self.label.setStyleSheet(f"color:{TEXT};")
        self.label.setWordWrap(True)
        l.addWidget(self.label)
        subscribe("transcript", self.on_transcript)
     # in LeftPanel
    def set_transcript(self, text: str):
      self.label.setText(f"TRANSCRIPTS\n{text}")

# in RightPanel
    def set_state(self, state: str):
      self.state.setText(f"STATE: {state}")

    def on_transcript(self, text):
        self.label.setText(f"TRANSCRIPTS\n{text}")

class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        l = QVBoxLayout(self)
        self.state = QLabel("STATE: IDLE")
        self.state.setStyleSheet(f"color:{TEXT};")
        l.addWidget(self.state)
        subscribe("state", self.on_state)

    def on_state(self, state):
        self.state.setText(f"STATE: {state}")
        if state == "LISTENING":
            self.state.setStyleSheet(f"color:{CYAN};")
        else:
            self.state.setStyleSheet(f"color:{TEXT};")
