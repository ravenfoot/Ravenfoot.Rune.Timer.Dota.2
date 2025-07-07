"""
Game Focus Utility: Brings the Dota 2 window to the foreground.

This function attempts to find and focus the Dota 2 game window using the Win32 API.
It assumes the window title is "Dota 2", which may need adjustment if localized or renamed.

Platform: Windows only
Dependencies: pywin32
"""

import win32gui
import win32con

def focus_dota2():
    """
    Attempt to bring the Dota 2 game window into focus.
    If the window is found, it is shown and activated.
    """
    hwnd = win32gui.FindWindow(None, "Dota 2")
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        win32gui.SetForegroundWindow(hwnd)
    else:
        print("[INFO] Dota 2 window not found.")
