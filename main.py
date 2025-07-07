"""
Main entry point for the Dota 2 Rune Timer application.

Launches the PyQt5 application and initializes the core timer modules:
- RuneTimer: Handles power, water, bounty, and wisdom rune timings
- RoshanTimer: Tracks Roshan's respawn schedule
- DayNightTimer: Monitors the Dota 2 day/night cycle

This script is the launch target for PyInstaller bundling and local development.
"""

import sys
from PyQt5.QtWidgets import QApplication

from gui.gui import MainWindow
from timers.rune_timer import RuneTimer
from timers.roshan_timer import RoshanTimer
from timers.daynight_timer import DayNightTimer

def main() -> None:
    """
    Initialize the application, inject timers into the GUI, and launch the event loop.
    """
    app = QApplication(sys.argv)

    rune_timer = RuneTimer()
    roshan_timer = RoshanTimer()
    daynight_timer = DayNightTimer()

    window = MainWindow(rune_timer, roshan_timer, daynight_timer)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
