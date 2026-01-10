import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QTimer


class CinematicCircle(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.glow_phase = 0.0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)  # ~60 FPS

    def tick(self):
        self.angle = (self.angle + 2) % 360
        self.glow_phase = (self.glow_phase + 0.02) % 1.0
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.fillRect(self.rect(), Qt.black)

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        r = min(w, h) // 3

        cyan = QColor(0, 255, 255)

        # Soft breathing glow
        glow_alpha = int(60 + 40 * abs(0.5 - self.glow_phase) * 2)
        glow_pen = QPen(QColor(0, 255, 255, glow_alpha), 16)
        p.setPen(glow_pen)
        p.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        # Main ring
        p.setPen(QPen(cyan, 4))
        p.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        # Rotating arc
        arc_r = r - 20
        p.setPen(QPen(cyan, 5))
        p.drawArc(
            cx - arc_r,
            cy - arc_r,
            arc_r * 2,
            arc_r * 2,
            self.angle * 16,
            90 * 16
        )


class Sandbox(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CASPER HUD SANDBOX — REFINED")
        self.resize(800, 800)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("CASPER")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: cyan;
            font-size: 28px;
            letter-spacing: 6px;
        """)

        circle = CinematicCircle()
        circle.setMinimumSize(500, 500)

        layout.addWidget(title)
        layout.addWidget(circle)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Sandbox()
    w.show()
    sys.exit(app.exec())
