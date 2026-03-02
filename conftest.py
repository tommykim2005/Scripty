"""
Root-level pytest configuration.

Stubs every platform-specific or display-dependent package *before* test
modules are collected, so utils/* can be imported on any OS (macOS, Linux,
Windows) without needing pyautogui, Win32 APIs, or a physical display.
"""
import sys
from unittest.mock import MagicMock

_PLATFORM_STUBS = [
    "pyautogui",
    "win32api",
    "win32con",
    "keyboard",
    "numpy",
    "customtkinter",
    "cv2",
]

for _mod in _PLATFORM_STUBS:
    sys.modules[_mod] = MagicMock(name=f"stub:{_mod}")
