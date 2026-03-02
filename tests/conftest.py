"""
Shared pytest configuration and fixtures.

Stubs out Windows-only modules (win32api, win32con) so the test suite can run
cross-platform (macOS, Linux, CI) without a Windows environment.  These stubs
are installed into sys.modules *before* any test file imports the project code,
ensuring that utils/click.py (which does ``import win32api, win32con``) won't
raise an ImportError on non-Windows hosts.
"""

import sys
from unittest.mock import MagicMock

for _mod in ("win32api", "win32con"):
    sys.modules.setdefault(_mod, MagicMock())
