from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QTimer


class CoreWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(400, 400)

        self.angle = 0
        self.glow = 0.0
        self.glow_dir = 1

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)

    def tick(self):
        self.angle = (self.angle + 4) % 360

        self.glow += 0.03 * self.glow_dir
        if self.glow >= 1.0:
            self.glow = 1.0
            self.glow_dir = -1
        elif self.glow <= 0.0:
            self.glow = 0.0
            self.glow_dir = 1

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.fillRect(self.rect(), Qt.black)

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        r = min(w, h) // 3

        cyan = QColor(0, 255, 255)

        glow_alpha = int(60 + 120 * self.glow)
        p.setPen(QPen(QColor(0, 255, 255, glow_alpha), 18))
        p.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        p.setPen(QPen(cyan, 4))
        p.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        arc_r = r - 25
        p.setPen(QPen(cyan, 8))
        p.drawArc(
            cx - arc_r,
            cy - arc_r,
            arc_r * 2,
            arc_r * 2,
            self.angle * 16,
            120 * 16
        )
        p.drawArc(
            cx - arc_r,
            cy - arc_r,
            arc_r * 2,
            arc_r * 2,
            (self.angle + 180) * 16,
            120 * 16
        )
        p.end()