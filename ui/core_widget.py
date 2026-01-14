from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QTimer, Signal


class CoreWidget(QWidget):
    stateChanged = Signal(str)

    def __init__(self):
        super().__init__()

        # ---------- Widget setup ----------
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(400, 400)

        # ---------- Animation state ----------
        self.angle = 0

        self.speed = 3               # rotation speed
        self.glow = 0.4              # current glow
        self.glow_target = 0.4        # target glow

        self.state = "IDLE"

        # ---------- Timer ----------
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)          # ~60 FPS

        # ---------- Signal ----------
        self.stateChanged.connect(self.set_state)

    # ======================================================
    # STATE HANDLING
    # ======================================================
    def set_state(self, state: str):
        self.state = state

        if state == "LISTENING":
            self.speed = 7
            self.glow_target = 1.0

        elif state == "PROCESSING":
            self.speed = 4
            self.glow_target = 0.7

        elif state == "SPEAKING":
            self.speed = 5
            self.glow_target = 1.2

        else:  # IDLE
            self.speed = 3
            self.glow_target = 0.4

    # ======================================================
    # ANIMATION TICK
    # ======================================================
    def tick(self):
    # ease rotation speed changes
      self._speed_current = getattr(self, "_speed_current", self.speed)
      self._speed_current += (self.speed - self._speed_current) * 0.15
      self.angle = (self.angle + self._speed_current) % 360

    # ease glow
      self.glow += (self.glow_target - self.glow) * 0.08
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
