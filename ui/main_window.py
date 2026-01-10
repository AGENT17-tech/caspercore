from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel
)
from PySide6.QtCore import Qt
from ui.core_widget import CoreWidget
from ui.panels import LeftPanel, RightPanel
from ui.theme import BG, CYAN


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.setStyleSheet(f"background-color: {BG};")

        central = QWidget()
        root = QHBoxLayout(central)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(20)

        self.left = LeftPanel()
        self.right = RightPanel()

        # ---- CENTER COLUMN (LOCKED) ----
        center = QWidget()
        center_layout = QVBoxLayout(center)
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setSpacing(12)

        title = QLabel("CASPER")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            color: {CYAN};
            font-size: 22px;
            letter-spacing: 6px;
            font-weight: 600;
        """)

        self.core = CoreWidget()
        self.core.setMinimumSize(500, 500)

        center_layout.addWidget(title)
        center_layout.addWidget(self.core, alignment=Qt.AlignCenter)

        # ---- ASSEMBLE ----
        root.addWidget(self.left, 2)
        root.addWidget(center, 3)
        root.addWidget(self.right, 2)

        self.setCentralWidget(central)
