# ui/banner.py
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class FloatingBanner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 60)
        self.move(100, 50)

        label = QLabel("Press ESC to stop the game", self)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        label.setStyleSheet("color: white; background-color: red; padding: 10px; border-radius: 10px;")
        label.setAlignment(Qt.AlignCenter)
        label.setFixedSize(400, 60)

    def show_temporary(self, duration_ms=5000):
        self.show()
        QTimer.singleShot(duration_ms, self.close)
