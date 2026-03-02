"""Verify that main.py can be imported as a module without triggering the
main execution block (i.e. the while-loop must be guarded by
``if __name__ == '__main__':``).
"""
import sys
import types
import importlib
import pytest
from unittest.mock import MagicMock, patch


def _stub(name: str) -> types.ModuleType:
    return types.ModuleType(name)


# Stub every platform/GUI dependency so the import doesn't crash on CI.
_STUBS = [
    "pyautogui", "win32api", "win32con", "keyboard", "numpy",
    "utils.finder",
]

@pytest.fixture(autouse=True)
def stub_dependencies():
    originals = {}
    for name in _STUBS:
        originals[name] = sys.modules.get(name)
        mod = _stub(name)
        # Give utils.finder stub the functions main.py imports
        if name == "utils.finder":
            mod.locate_on_screen = MagicMock(return_value=True)
            mod.pixel_check = MagicMock(return_value=True)
        sys.modules[name] = mod

    # Remove any cached main module so we always re-import fresh.
    sys.modules.pop("main", None)
    yield
    for name, orig in originals.items():
        if orig is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = orig
    sys.modules.pop("main", None)


def test_main_importable_without_execution():
    """Importing main should not start the while-loop."""
    # If the while-loop runs it would block forever (locate_on_screen would
    # need to be called). We verify it is NOT called during plain import.
    import main  # noqa: F401
    finder_mod = sys.modules["utils.finder"]
    finder_mod.locate_on_screen.assert_not_called()
