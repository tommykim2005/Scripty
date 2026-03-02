"""
Tests for the screen-location loop in main.py.

main.py contains module-level code (a while loop that retries locate_on_screen
until it succeeds).  Each test re-executes that code in isolation via
runpy.run_path so that side effects don't leak between test runs.

Dependencies (locate_on_screen, time.sleep) are fully mocked; no real screen
access or delays occur.
"""

import os
import runpy
from unittest.mock import patch, call

# Resolve main.py relative to this file so the tests work regardless of the
# current working directory when pytest is invoked.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MAIN_PY = os.path.join(_REPO_ROOT, "main.py")


def _run_main(locate_side_effects):
    """
    Execute main.py with locate_on_screen returning the given side_effects
    sequence and time.sleep stubbed out.

    Returns (mock_locate, mock_sleep, captured_stdout_text).
    """
    with patch("utils.finder.locate_on_screen",
               side_effect=locate_side_effects) as mock_loc, \
         patch("time.sleep") as mock_sleep, \
         patch("builtins.print") as mock_print:
        runpy.run_path(_MAIN_PY, run_name="__main__")

    printed = " ".join(
        str(a) for call_ in mock_print.call_args_list for a in call_[0]
    )
    return mock_loc, mock_sleep, printed


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_success_on_first_attempt():
    """locate_on_screen succeeds immediately: no retries, no sleep."""
    mock_loc, mock_sleep, output = _run_main([True])

    mock_loc.assert_called_once_with("images/coin.png")
    mock_sleep.assert_not_called()
    assert "Success" in output


def test_retries_once_then_succeeds():
    """One failure followed by success: sleep called once with 0.5 s."""
    mock_loc, mock_sleep, output = _run_main([False, True])

    assert mock_loc.call_count == 2
    mock_sleep.assert_called_once_with(0.5)
    assert "Could not locate retrying" in output
    assert "Success" in output


def test_retries_multiple_times_then_succeeds():
    """Multiple failures: sleep is called once per failed attempt."""
    failures = 4
    mock_loc, mock_sleep, output = _run_main([False] * failures + [True])

    assert mock_loc.call_count == failures + 1
    assert mock_sleep.call_count == failures
    assert "Success" in output


def test_retry_sleep_uses_half_second_interval():
    """Each retry waits exactly 0.5 seconds."""
    mock_loc, mock_sleep, _ = _run_main([False, False, True])

    expected_calls = [call(0.5), call(0.5)]
    assert mock_sleep.call_args_list == expected_calls


def test_image_path_is_coin_png():
    """main.py always searches for 'images/coin.png'."""
    mock_loc, _, _ = _run_main([True])

    args, _ = mock_loc.call_args
    assert args[0] == "images/coin.png"


def test_retry_message_printed_on_each_failure():
    """'Could not locate retrying' is printed exactly once per failed attempt."""
    mock_loc, mock_sleep, output = _run_main([False, False, True])

    # Two failures → message should appear twice in the output.
    assert output.count("Could not locate retrying") == 2
