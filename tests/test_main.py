"""
Minimal smoke test for main.py

main.py runs a blocking while-loop at module scope that calls
utils.finder.locate_on_screen().  To safely import it in a test we must:

  1. Stub all Windows / display dependencies (done globally in conftest.py).
  2. Patch utils.finder so locate_on_screen() returns True immediately,
     which causes the while-loop to exit after a single iteration.

The test simply asserts that the module loads and executes without raising
an unhandled exception.
"""

import sys
import importlib
from unittest.mock import MagicMock, patch

import pytest


def _build_finder_stub(locate_return=True):
    """Return a MagicMock that mimics utils.finder."""
    stub = MagicMock()
    stub.locate_on_screen.return_value = locate_return
    stub.pixel_check.return_value = True
    return stub


@pytest.fixture()
def finder_stub(monkeypatch):
    """Inject a finder stub and clean up afterwards."""
    stub = _build_finder_stub(locate_return=True)
    monkeypatch.setitem(sys.modules, "utils.finder", stub)
    monkeypatch.setitem(sys.modules, "utils.click", MagicMock())
    monkeypatch.setitem(sys.modules, "utils.human_move", MagicMock())
    # Ensure a fresh import of main on each test run
    sys.modules.pop("main", None)
    yield stub


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_main_imports_without_error(finder_stub):
    """
    main.py should import (and its top-level while-loop should complete)
    without raising any exception when dependencies are properly stubbed.
    """
    import main  # noqa: PLC0415
    # Reaching this line means main ran to completion without error.
    assert True


def test_main_calls_locate_on_screen(finder_stub):
    """
    The while-loop in main.py must call locate_on_screen at least once.
    """
    import main  # noqa: PLC0415
    finder_stub.locate_on_screen.assert_called()
