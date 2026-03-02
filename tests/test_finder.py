"""
Tests for utils/finder.py

Covers:
  - locate_on_screen: success path, image-not-found (falsy box), ImageNotFoundException,
    confidence parameter forwarding.
  - pixel_check: colour-match / no-match for all three RGB channels, coordinate
    forwarding to pyautogui.pixel.

All calls that would touch the screen (pyautogui, click, human_move_curved) are
fully mocked so the suite runs without a display or Windows environment.
"""

import pyautogui
import pytest
from unittest.mock import patch, MagicMock, call

from utils.finder import locate_on_screen, pixel_check


# ---------------------------------------------------------------------------
# locate_on_screen
# ---------------------------------------------------------------------------

class TestLocateOnScreen:

    def test_returns_true_when_image_found(self):
        """Successful location moves the cursor into the box and returns True."""
        fake_box = MagicMock()
        fake_box.left = 100
        fake_box.top = 200
        fake_box.width = 50
        fake_box.height = 30

        with patch("pyautogui.locateOnScreen", return_value=fake_box), \
             patch("utils.finder.human_move_curved") as mock_move, \
             patch("utils.finder.click.click") as mock_click:
            result = locate_on_screen("images/test.png")

        assert result is True
        mock_move.assert_called_once()
        mock_click.assert_called_once()

        # Click coordinates must fall inside the bounding box.
        clicked_x, clicked_y = mock_click.call_args[0]
        assert fake_box.left <= clicked_x <= fake_box.left + fake_box.width - 1
        assert fake_box.top <= clicked_y <= fake_box.top + fake_box.height - 1

    def test_returns_false_when_box_is_none(self):
        """When locateOnScreen returns None the function returns False without clicking."""
        with patch("pyautogui.locateOnScreen", return_value=None), \
             patch("utils.finder.human_move_curved") as mock_move, \
             patch("utils.finder.click.click") as mock_click:
            result = locate_on_screen("images/test.png")

        assert result is False
        mock_move.assert_not_called()
        mock_click.assert_not_called()

    def test_returns_false_when_box_is_falsy(self):
        """Any falsy return from locateOnScreen (e.g. empty tuple) is treated as not found."""
        with patch("pyautogui.locateOnScreen", return_value=()), \
             patch("utils.finder.human_move_curved") as mock_move, \
             patch("utils.finder.click.click") as mock_click:
            result = locate_on_screen("images/test.png")

        assert result is False
        mock_move.assert_not_called()
        mock_click.assert_not_called()

    def test_returns_false_on_image_not_found_exception(self):
        """ImageNotFoundException is caught and results in False with no side effects."""
        with patch("pyautogui.locateOnScreen",
                   side_effect=pyautogui.ImageNotFoundException), \
             patch("utils.finder.human_move_curved") as mock_move, \
             patch("utils.finder.click.click") as mock_click:
            result = locate_on_screen("images/test.png")

        assert result is False
        mock_move.assert_not_called()
        mock_click.assert_not_called()

    def test_default_confidence_is_0_8(self):
        """The default confidence value forwarded to pyautogui is 0.8."""
        with patch("pyautogui.locateOnScreen", return_value=None) as mock_locate, \
             patch("utils.finder.human_move_curved"), \
             patch("utils.finder.click.click"):
            locate_on_screen("images/test.png")

        _, kwargs = mock_locate.call_args
        assert kwargs["confidence"] == 0.8

    def test_custom_confidence_is_forwarded(self):
        """A caller-supplied confidence value is passed through unchanged."""
        with patch("pyautogui.locateOnScreen", return_value=None) as mock_locate, \
             patch("utils.finder.human_move_curved"), \
             patch("utils.finder.click.click"):
            locate_on_screen("images/test.png", confidence=0.95)

        _, kwargs = mock_locate.call_args
        assert kwargs["confidence"] == 0.95

    def test_grayscale_flag_is_always_true(self):
        """locate_on_screen always uses grayscale=True for efficiency."""
        with patch("pyautogui.locateOnScreen", return_value=None) as mock_locate, \
             patch("utils.finder.human_move_curved"), \
             patch("utils.finder.click.click"):
            locate_on_screen("images/test.png")

        _, kwargs = mock_locate.call_args
        assert kwargs["grayscale"] is True

    def test_image_path_is_forwarded(self):
        """The image path argument is passed verbatim to pyautogui.locateOnScreen."""
        with patch("pyautogui.locateOnScreen", return_value=None) as mock_locate, \
             patch("utils.finder.human_move_curved"), \
             patch("utils.finder.click.click"):
            locate_on_screen("images/special_image.png")

        positional_args = mock_locate.call_args[0]
        assert positional_args[0] == "images/special_image.png"


# ---------------------------------------------------------------------------
# pixel_check
# ---------------------------------------------------------------------------

class TestPixelCheck:

    def test_red_channel_match_returns_true(self):
        """pixel_check returns True when the red channel (index 0) matches."""
        with patch("pyautogui.pixel", return_value=(255, 128, 64)):
            assert pixel_check(10, 20, 0, 255) is True

    def test_red_channel_no_match_returns_false(self):
        """pixel_check returns False when the red channel does not match."""
        with patch("pyautogui.pixel", return_value=(100, 128, 64)):
            assert pixel_check(10, 20, 0, 255) is False

    def test_green_channel_match_returns_true(self):
        """pixel_check returns True when the green channel (index 1) matches."""
        with patch("pyautogui.pixel", return_value=(0, 200, 0)):
            assert pixel_check(5, 5, 1, 200) is True

    def test_green_channel_no_match_returns_false(self):
        """pixel_check returns False when the green channel does not match."""
        with patch("pyautogui.pixel", return_value=(0, 200, 0)):
            assert pixel_check(5, 5, 1, 150) is False

    def test_blue_channel_match_returns_true(self):
        """pixel_check returns True when the blue channel (index 2) matches."""
        with patch("pyautogui.pixel", return_value=(0, 0, 77)):
            assert pixel_check(0, 0, 2, 77) is True

    def test_blue_channel_no_match_returns_false(self):
        """pixel_check returns False when the blue channel does not match."""
        with patch("pyautogui.pixel", return_value=(0, 0, 77)):
            assert pixel_check(0, 0, 2, 99) is False

    def test_coordinates_forwarded_to_pyautogui(self):
        """pixel_check passes (x, y) to pyautogui.pixel unchanged."""
        with patch("pyautogui.pixel", return_value=(0, 0, 0)) as mock_pixel:
            pixel_check(42, 99, 0, 0)

        mock_pixel.assert_called_once_with(42, 99)
