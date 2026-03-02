"""
Tests for utils/human_move.py

Covers:
  - _fitts_duration: pure-math calculations, edge-case clamping, formula correctness.
  - human_move:      moveTo call count, target coordinates, explicit vs auto duration,
                     default easing function.
  - human_move_curved: two-segment movement, correct final target, explicit duration
                       path, minimum d2 floor.

pyautogui.position / moveTo are mocked so nothing touches the actual mouse.
random.uniform and random.randint are mocked where deterministic behaviour is
needed.
"""

import math
import pyautogui
import pytest
from unittest.mock import patch, call, MagicMock

from utils.human_move import _fitts_duration, human_move, human_move_curved


# ---------------------------------------------------------------------------
# _fitts_duration  (pure computation — no mocking required)
# ---------------------------------------------------------------------------

class TestFittsDuration:

    def test_returns_positive_value(self):
        assert _fitts_duration(200.0, 40.0) > 0

    def test_longer_distance_gives_longer_duration(self):
        assert _fitts_duration(500.0, 40.0) > _fitts_duration(50.0, 40.0)

    def test_larger_target_gives_shorter_duration(self):
        """A wider/easier target should require less movement time."""
        assert _fitts_duration(200.0, 100.0) < _fitts_duration(200.0, 10.0)

    def test_distance_clamped_to_minimum_1(self):
        """Distances < 1 are clamped to 1.0 to avoid log(0) / log(negative)."""
        assert _fitts_duration(0.0, 40.0) == pytest.approx(_fitts_duration(1.0, 40.0))
        assert _fitts_duration(-50.0, 40.0) == pytest.approx(_fitts_duration(1.0, 40.0))

    def test_target_width_clamped_to_minimum_4(self):
        """target_width_px < 4 is clamped to 4.0."""
        assert _fitts_duration(200.0, 0.0) == pytest.approx(_fitts_duration(200.0, 4.0))
        assert _fitts_duration(200.0, -10.0) == pytest.approx(_fitts_duration(200.0, 4.0))

    def test_formula_correctness(self):
        """Verify the exact formula: a + b * log2(dist / width + 1)."""
        a, b = 0.12, 0.085
        dist, width = 100.0, 40.0
        expected = a + b * math.log2(dist / width + 1.0)
        assert _fitts_duration(dist, width, a=a, b=b) == pytest.approx(expected)

    def test_custom_a_and_b_parameters(self):
        """Custom intercept and slope parameters are respected."""
        result = _fitts_duration(100.0, 40.0, a=0.5, b=0.0)
        assert result == pytest.approx(0.5)  # b=0 → result == a


# ---------------------------------------------------------------------------
# human_move
# ---------------------------------------------------------------------------

class TestHumanMove:

    def test_calls_moveto_exactly_once(self):
        with patch("pyautogui.position", return_value=(0, 0)), \
             patch("pyautogui.moveTo") as mock_move, \
             patch("random.uniform", return_value=1.0):
            human_move(100, 200)

        mock_move.assert_called_once()

    def test_moveto_receives_correct_target_coordinates(self):
        with patch("pyautogui.position", return_value=(0, 0)), \
             patch("pyautogui.moveTo") as mock_move, \
             patch("random.uniform", return_value=1.0):
            human_move(300, 400)

        args, _ = mock_move.call_args
        assert args[0] == 300
        assert args[1] == 400

    def test_explicit_duration_is_used_verbatim(self):
        """When a duration is supplied, it is passed straight to moveTo."""
        with patch("pyautogui.position", return_value=(0, 0)), \
             patch("pyautogui.moveTo") as mock_move, \
             patch("random.uniform") as mock_rand:
            human_move(50, 50, duration=0.75)

        _, kwargs = mock_move.call_args
        assert kwargs["duration"] == pytest.approx(0.75)
        # random.uniform must NOT be called when duration is provided explicitly.
        mock_rand.assert_not_called()

    def test_auto_duration_is_positive(self):
        """When duration is omitted, the computed value is always positive."""
        with patch("pyautogui.position", return_value=(0, 0)), \
             patch("pyautogui.moveTo") as mock_move, \
             patch("random.uniform", return_value=1.0):
            human_move(200, 300)

        _, kwargs = mock_move.call_args
        assert kwargs["duration"] > 0

    def test_default_easing_function_is_forwarded(self):
        """The easeInOutQuad tween is forwarded to moveTo by default."""
        with patch("pyautogui.position", return_value=(0, 0)), \
             patch("pyautogui.moveTo") as mock_move, \
             patch("random.uniform", return_value=1.0):
            human_move(100, 100)

        _, kwargs = mock_move.call_args
        assert kwargs.get("tween") is pyautogui.easeInOutQuad

    def test_custom_easing_function_is_forwarded(self):
        """A caller-supplied easing function is forwarded instead of the default."""
        custom_easing = MagicMock(name="custom_easing")
        with patch("pyautogui.position", return_value=(0, 0)), \
             patch("pyautogui.moveTo") as mock_move, \
             patch("random.uniform", return_value=1.0):
            human_move(100, 100, easing=custom_easing)

        _, kwargs = mock_move.call_args
        assert kwargs.get("tween") is custom_easing


# ---------------------------------------------------------------------------
# human_move_curved
# ---------------------------------------------------------------------------

class TestHumanMoveCurved:

    def test_calls_moveto_exactly_twice(self):
        """Curved path = midpoint move + final-target move."""
        with patch("pyautogui.position", return_value=(0, 0)), \
             patch("pyautogui.moveTo") as mock_move, \
             patch("random.uniform", return_value=0.5), \
             patch("random.randint", return_value=0):
            human_move_curved(200, 300)

        assert mock_move.call_count == 2

    def test_second_moveto_reaches_destination(self):
        """The second moveTo call must target the caller-supplied (x, y)."""
        with patch("pyautogui.position", return_value=(0, 0)), \
             patch("pyautogui.moveTo") as mock_move, \
             patch("random.uniform", return_value=0.5), \
             patch("random.randint", return_value=0):
            human_move_curved(200, 300)

        second_args = mock_move.call_args_list[1][0]
        assert second_args[0] == 200
        assert second_args[1] == 300

    def test_explicit_duration_skips_fitts_calculation(self):
        """Supplying a duration bypasses _fitts_duration entirely."""
        with patch("pyautogui.position", return_value=(0, 0)), \
             patch("pyautogui.moveTo"), \
             patch("utils.human_move._fitts_duration") as mock_fitts, \
             patch("random.uniform", return_value=0.5), \
             patch("random.randint", return_value=0):
            human_move_curved(100, 100, duration=1.0)

        mock_fitts.assert_not_called()

    def test_d1_plus_d2_equals_explicit_duration(self):
        """With random.uniform == 0.5, d1 = 0.5*T and d2 = T - d1, sum == T."""
        total = 1.0
        with patch("pyautogui.position", return_value=(0, 0)), \
             patch("pyautogui.moveTo") as mock_move, \
             patch("random.uniform", return_value=0.5), \
             patch("random.randint", return_value=0):
            human_move_curved(100, 100, duration=total)

        d1 = mock_move.call_args_list[0][1]["duration"]
        d2 = mock_move.call_args_list[1][1]["duration"]
        assert d1 + d2 == pytest.approx(total)

    def test_d2_floor_is_enforced(self):
        """d2 must be at least 0.05 seconds regardless of d1."""
        # With uniform→0.9999, d1 ≈ total; d2 = max(0.05, total - d1) = 0.05.
        with patch("pyautogui.position", return_value=(0, 0)), \
             patch("pyautogui.moveTo") as mock_move, \
             patch("random.uniform", return_value=0.9999), \
             patch("random.randint", return_value=0):
            human_move_curved(1, 1, duration=0.001)

        d2 = mock_move.call_args_list[1][1]["duration"]
        assert d2 >= 0.05

    def test_segment_durations_are_positive(self):
        """Both movement segments must have a positive duration."""
        with patch("pyautogui.position", return_value=(0, 0)), \
             patch("pyautogui.moveTo") as mock_move, \
             patch("random.uniform", return_value=0.5), \
             patch("random.randint", return_value=0):
            human_move_curved(150, 250)

        d1 = mock_move.call_args_list[0][1]["duration"]
        d2 = mock_move.call_args_list[1][1]["duration"]
        assert d1 > 0
        assert d2 > 0
