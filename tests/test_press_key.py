"""Tests for utils/press_key.py

pyautogui and win32 dependencies are mocked so the suite runs on any
platform / CI environment without a display.
"""
import sys
import types
import time
import pytest
from unittest.mock import MagicMock, patch, call


# ---------------------------------------------------------------------------
# Stub out platform-specific modules before importing press_key
# ---------------------------------------------------------------------------

def _make_stub(name: str) -> types.ModuleType:
    mod = types.ModuleType(name)
    return mod


for _name in ("pyautogui", "win32api", "win32con", "keyboard"):
    if _name not in sys.modules:
        sys.modules[_name] = _make_stub(_name)


# Now safe to import
from utils import press_key, globals  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

HOLD_VAL = 0.07
DELAY_VAL = 0.10


@pytest.fixture(autouse=True)
def patch_globals(monkeypatch):
    """Make random helpers return deterministic values for assertions."""
    monkeypatch.setattr(globals, "random_hold", lambda: HOLD_VAL)
    monkeypatch.setattr(globals, "random_delay", lambda: DELAY_VAL)


# ---------------------------------------------------------------------------
# Tests: human_press
# ---------------------------------------------------------------------------

class TestHumanPress:
    def test_calls_keydown_and_keyup(self):
        with patch("utils.press_key.pyautogui") as mock_pag, \
             patch("utils.press_key.time") as mock_time:
            press_key.human_press("a")
            mock_pag.keyDown.assert_called_once_with("a")
            mock_pag.keyUp.assert_called_once_with("a")

    def test_sleep_called_with_return_values(self):
        """time.sleep must receive the *return value* of the globals functions,
        not a function object."""
        with patch("utils.press_key.pyautogui"), \
             patch("utils.press_key.time") as mock_time:
            press_key.human_press("b")
            sleep_args = [c.args[0] for c in mock_time.sleep.call_args_list]
            # Both sleep arguments must be floats (not callables)
            for arg in sleep_args:
                assert isinstance(arg, float), (
                    f"time.sleep received {type(arg)} instead of float — "
                    "globals helper was not called"
                )

    def test_sleep_uses_correct_values(self):
        """Ensure the patched deterministic values reach time.sleep."""
        with patch("utils.press_key.pyautogui"), \
             patch("utils.press_key.time") as mock_time:
            press_key.human_press("c")
            calls = mock_time.sleep.call_args_list
            assert calls[0] == call(HOLD_VAL), f"First sleep should be random_hold() = {HOLD_VAL}"
            assert calls[1] == call(DELAY_VAL), f"Second sleep should be random_delay() = {DELAY_VAL}"

    def test_keydown_before_keyup(self):
        """keyDown must be called before keyUp."""
        order = []
        with patch("utils.press_key.pyautogui") as mock_pag, \
             patch("utils.press_key.time"):
            mock_pag.keyDown.side_effect = lambda k: order.append("down")
            mock_pag.keyUp.side_effect = lambda k: order.append("up")
            press_key.human_press("d")
        assert order == ["down", "up"]


# ---------------------------------------------------------------------------
# Tests: human_type
# ---------------------------------------------------------------------------

class TestHumanType:
    def test_calls_human_press_for_each_char(self):
        with patch("utils.press_key.human_press") as mock_hp:
            press_key.human_type("hi")
            assert mock_hp.call_count == 2
            mock_hp.assert_any_call("h")
            mock_hp.assert_any_call("i")

    def test_empty_string_no_calls(self):
        with patch("utils.press_key.human_press") as mock_hp:
            press_key.human_type("")
            mock_hp.assert_not_called()

    def test_single_char(self):
        with patch("utils.press_key.human_press") as mock_hp:
            press_key.human_type("x")
            mock_hp.assert_called_once_with("x")
