"""
OverlayManager: Displays transparent top-center image overlays in-game.

Used for showing rune warnings in Dota 2 via .png icons.
Requires the game to be in borderless or windowed mode for visibility.
Built with PyQt5 for full transparency and always-on-top display.
"""

import os
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

class OverlayManager(QWidget):
    """
    Manages an always-on-top transparent overlay that displays rune alert images.
    """

    def __init__(self, warnings_path: str, parent=None):
        """
        Args:
            warnings_path (str): Path to folder containing .png rune alert images.
            parent (QWidget, optional): Parent widget (default is None).
        """
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowStaysOnTopHint |
                            Qt.FramelessWindowHint |
                            Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background: transparent;")

        self.warnings_path = warnings_path
        self.hide()

    def show_rune_warning(self, image_name: str, duration_ms: int = 5000) -> None:
        """
        Display an overlay image centered near the top of the screen.

        Args:
            image_name (str): Filename of the .png image.
            duration_ms (int): Duration in milliseconds to display the overlay.
        """
        full_path = os.path.join(self.warnings_path, image_name)
        pixmap = QPixmap(full_path)

        if pixmap.isNull():
            print(f"[WARNING] Could not load overlay image: {full_path}")
            return

        self.label.setPixmap(pixmap)
        self.label.adjustSize()
        self.resize(self.label.width(), self.label.height())

        screen_geo = self.screen().availableGeometry()
        x = (screen_geo.width() - self.width()) // 2
        self.move(x, 50)  # 50px offset from top for better visibility

        self.show()
        QTimer.singleShot(duration_ms, self.hide_overlay)

    def hide_overlay(self) -> None:
        """
        Hide the overlay window.
        """
        self.hide()
