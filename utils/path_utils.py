"""
Path Utility for Resource Access

This module defines a helper function `resource_path()` to locate asset files (e.g. icons, sounds)
regardless of whether the program is running in a normal Python environment or inside a PyInstaller bundle.

Usage:
    resource_path("assets/icons/timer_icon.ico")

Ensures compatibility with both development and deployment scenarios.
"""

import sys
import os

def resource_path(relative_path: str) -> str:
    """
    Generate an absolute file path to the given resource.

    Supports both standard Python runs and PyInstaller onefile builds.

    Args:
        relative_path (str): Path to the resource from the project root

    Returns:
        str: Absolute path to the resource on the filesystem
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        base_path = os.path.dirname(__file__)
        return os.path.join(base_path, '..', relative_path)
