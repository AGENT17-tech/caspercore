from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QTimer, Signal
import math
import time

STATE_PROFILES = {
    "IDLE": {
        "speed": 0.15,
        "glow": 0.25,
        "pulse": 0.0,
    },
    "LISTENING": {
        "speed": 0.45,
        "glow": 0.55,
        "pulse": 0.15,
    },
    "PROCESSING": {
        "speed": 1.1,
        "glow": 0.9,
        "pulse": 0.35,
    },
    "SPEAKING": {
        "speed": 0.7,
        "glow": 0.75,
        "pulse": 0.25,
    },
}



class CoreWidget(QWidget):
    stateChanged = Signal(str)

    def __init__(self):
        super().__init__()

        # ---------- Widget setup ----------
        self.angle = 0.0

        self.speed = 0.15
        self.glow = 0.25
        self.pulse = 0.0

        # smooth targets
        self._speed_target = self.speed
        self._glow_target = self.glow
        self._pulse_target = self.pulse
        self._t0 = time.time()
        # ---------- Signal ----------
        self.stateChanged.connect(self.set_state)

    # ======================================================
    # STATE HANDLING
    # ======================================================
    def set_state(self, state: str):
        profile = STATE_PROFILES.get(state, STATE_PROFILES["IDLE"])

        self._speed_target = profile["speed"]
        self._glow_target = profile["glow"]
        self._pulse_target = profile["pulse"]

    # ======================================================
    # ANIMATION TICK
    # ======================================================
    def tick(self):
    # smooth easing
       self.speed += (self._speed_target - self.speed) * 0.12
       self.glow += (self._glow_target - self.glow) * 0.08
       self.pulse += (self._pulse_target - self.pulse) * 0.10

    # rotation
       self.angle = (self.angle + self.speed) % 360

    # breathing glow (very subtle)
       t = time.time() - self._t0
       self.breath = 0.06 * math.sin(t * 2.0)

       self.update()



    # ======================================================
    # PAINT
    # ======================================================
    def paintEvent(self, event):
        
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
       
        # Background
        p.fillRect(self.rect(), Qt.black)

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 3

        cyan = QColor(0, 255, 255)

        # ---------- Outer glow ----------
        glow_alpha = int(50 + 120 * self.glow)
        p.setPen(QPen(QColor(0, 255, 255, glow_alpha), 18))
        p.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)

        # ---------- Core ring ----------
        p.setPen(QPen(cyan, 4))
        p.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)
        effective_glow = self.glow + self.breath
        inner_r = radius - 12 - int(6 * effective_glow)
        p.setPen(QPen(QColor(0, 255, 255, int(200 * effective_glow)), 6))
        p.drawEllipse(cx - inner_r, cy - inner_r, inner_r * 2, inner_r * 2)
        # ---------- Rotating arc ----------
        arc_r = radius - 26
        p.setPen(QPen(cyan, 8))
        p.drawArc(
            cx - arc_r,
            cy - arc_r,
            arc_r * 2,
            arc_r * 2,
            int(self.angle * 16),
            int(120 * 16)
        )

        # ---------- Center dot ----------
        p.setPen(Qt.NoPen)
        p.setBrush(cyan)
        p.drawEllipse(cx - 4, cy - 4, 8, 8)

        p.end()
