import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QTimer, Qt

# -------------------------------
# Project-specific modules
# -------------------------------
from utils.sound_manager import play_rune_sounds
from utils.game_focus import focus_dota2
from utils.overlay_manager import OverlayManager
from utils.path_utils import resource_path

"""
Main GUI interface for the Dota 2 Rune Timer application.

Features:
- Visual timer synced with in-game time (-1:00 start)
- Start/Pause/Reset controls
- Overlays and audio alerts for runes, Roshan, and day-night cycles
- Compatible with PyInstaller onefile builds

Dependencies:
- PyQt5, custom `utils` and `timers` modules
- Resource files in /assets and /gui

Designed for modularity and integration with Dota 2.
"""

# -------------------------------
# Asset and style paths
# -------------------------------
ASSET_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
ICON_DIR = os.path.join(ASSET_DIR, 'icons')
STYLE_PATH = os.path.join(os.path.dirname(__file__), 'style.css')  # Deprecated if using resource_path
WARNINGS_PATH = os.path.join(ASSET_DIR, 'warnings')

class MainWindow(QMainWindow):
    """
    The main GUI window for the Dota 2 Timer application.
    Displays a timer, handles GUI interaction, and integrates with sound/overlay modules.
    """

    RUNE_IMAGE_MAP = {
        "Bounty_Rune": "bounty_soon.png",
        "Power_Rune":  "power_soon.png",
        "Water_Rune":  "water_soon.png",
        "Wisdom_Rune": "wisdom_soon.png"
    }

    def __init__(self, rune_timer, roshan_timer, daynight_timer):
        """
        :param rune_timer: Instance of RuneTimer
        :param roshan_timer: Instance of RoshanTimer
        :param daynight_timer: Instance of DayNightTimer
        """
        super().__init__()

        self.rune_timer = rune_timer
        self.roshan_timer = roshan_timer
        self.daynight_timer = daynight_timer

        self.setWindowTitle("Dota 2 Rune Timer")
        icon_path = resource_path("assets/icons/timer_icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.current_time = -60  # Game-time starts at -1:00
        self.running = False

        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.timer_label = QLabel(self.format_time(self.current_time))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 30, QFont.Bold))
        layout.addWidget(self.timer_label)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)
        layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_timer)
        layout.addWidget(self.pause_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)
        layout.addWidget(self.reset_button)

        # Safely attempt to load styles
        try:
            style_file = resource_path("gui/style.css")
            with open(style_file, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("[WARNING] style.css not found. Continuing with default styles.")

        self.qtimer = QTimer()
        self.qtimer.timeout.connect(self.update_timer)

        self.resize(300, 200)

        self.overlay_manager = OverlayManager(resource_path("assets/warnings"))

    def start_timer(self):
        """Start/resume the timer if not already running, and focus the Dota 2 window."""
        if not self.running:
            self.running = True
            self.qtimer.start(1000)
            focus_dota2()

    def pause_timer(self):
        """Pause the timer."""
        self.running = False
        self.qtimer.stop()

    def reset_timer(self):
        """Reset the timer to -60 and update the display."""
        self.pause_timer()
        self.current_time = -60
        self.timer_label.setText(self.format_time(self.current_time))

    def update_timer(self):
        """Increment the timer by 1 second and evaluate alerts."""
        self.current_time += 1
        self.timer_label.setText(self.format_time(self.current_time))
        self.check_events()

    def check_events(self):
        """Aggregate alerts from all timers and trigger sound/overlay notifications."""
        game_time = self.current_time
        alerts = []

        try:
            alerts += self.rune_timer.get_alerts(game_time)
            alerts += self.roshan_timer.get_alerts(game_time)
            alerts += self.daynight_timer.get_alerts(game_time)
        except Exception as e:
            print(f"[ERROR] Failed to get alerts: {e}")

        if alerts:
            play_rune_sounds(alerts)
            self.show_rune_overlays(alerts)

    def show_rune_overlays(self, rune_list):
        """Show overlays for upcoming rune spawns."""
        for r in rune_list:
            png_name = self.RUNE_IMAGE_MAP.get(r, None)
            if png_name:
                self.overlay_manager.show_rune_warning(png_name, duration_ms=5000)

    def format_time(self, secs: int) -> str:
        """Format seconds into mm:ss, with a leading minus if negative."""
        sign = "-" if secs < 0 else ""
        s = abs(secs)
        m = s // 60
        s = s % 60
        return f"{sign}{m}:{s:02d}"
