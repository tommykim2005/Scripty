"""
Smoke tests for utils/press_key.py

pyautogui is stubbed by conftest.py so no real keyboard events are sent and
no display is required.  time.sleep is further patched inside each test so
the suite runs instantly.

Known bug (tracked for follow-up, NOT fixed here):
    press_key.py calls:
        time.sleep(globals.random_hold)   # missing () — passes function object
        time.sleep(globals.random_delay)  # missing () — passes function object
    At runtime this raises TypeError because time.sleep expects a number.
    The bug is masked in tests because time.sleep itself is mocked.
"""

import importlib
import sys
from unittest.mock import MagicMock, call, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_press_key():
    """(Re-)import utils.press_key under the current sys.modules mocks."""
    sys.modules.pop("utils.press_key", None)
    import utils.press_key as pk  # noqa: PLC0415
    return pk


# ---------------------------------------------------------------------------
# Structural / importability tests
# ---------------------------------------------------------------------------

def test_module_imports_without_error():
    """utils.press_key should be importable when pyautogui is stubbed."""
    pk = _load_press_key()
    assert pk is not None


def test_human_press_is_callable():
    pk = _load_press_key()
    assert callable(pk.human_press)


def test_human_type_is_callable():
    pk = _load_press_key()
    assert callable(pk.human_type)


# ---------------------------------------------------------------------------
# Behavioural tests (pyautogui + time fully mocked)
# ---------------------------------------------------------------------------

def test_human_press_calls_keydown_then_keyup():
    """human_press should call keyDown then keyUp for the given key."""
    pk = _load_press_key()
    mock_pag = sys.modules["pyautogui"]
    mock_pag.reset_mock()

    with patch("time.sleep"):
        pk.human_press("a")

    mock_pag.keyDown.assert_called_once_with("a")
    mock_pag.keyUp.assert_called_once_with("a")


def test_human_press_keydown_before_keyup():
    """keyDown must be called before keyUp (order matters)."""
    pk = _load_press_key()
    mock_pag = sys.modules["pyautogui"]
    mock_pag.reset_mock()
    call_order = []
    mock_pag.keyDown.side_effect = lambda k: call_order.append(("keyDown", k))
    mock_pag.keyUp.side_effect = lambda k: call_order.append(("keyUp", k))

    with patch("time.sleep"):
        pk.human_press("b")

    assert call_order == [("keyDown", "b"), ("keyUp", "b")]


def test_human_type_presses_each_character():
    """human_type should send a keyDown+keyUp pair per character."""
    pk = _load_press_key()
    mock_pag = sys.modules["pyautogui"]
    mock_pag.reset_mock()

    with patch("time.sleep"):
        pk.human_type(["x", "y", "z"])

    assert mock_pag.keyDown.call_count == 3
    assert mock_pag.keyUp.call_count == 3
    mock_pag.keyDown.assert_any_call("x")
    mock_pag.keyDown.assert_any_call("y")
    mock_pag.keyDown.assert_any_call("z")


def test_human_type_empty_sequence_does_nothing():
    """human_type with an empty list should not call any pyautogui methods."""
    pk = _load_press_key()
    mock_pag = sys.modules["pyautogui"]
    mock_pag.reset_mock()

    with patch("time.sleep"):
        pk.human_type([])

    mock_pag.keyDown.assert_not_called()
    mock_pag.keyUp.assert_not_called()
