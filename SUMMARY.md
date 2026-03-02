# Change Summary

## Overview

This PR merges the `dev` branch into `main`, bringing in the automated pytest
test suite that was developed after the round-2 bug fixes landed on `main`.

---

## Changes Made

### Bug Fixes (already on `main` via PR #10)

These fixes were applied in previous PRs and are included here for completeness.

#### `utils/finder.py` — Off-by-one in random click coordinates
- `random.randint(box.left, box.left + box.width)` could select a pixel one
  pixel outside the matched image region. Changed to `box.width - 1` and
  `box.height - 1` to stay within valid bounds.

#### `utils/finder.py` — Docstring parameter name mismatch in `pixel_check`
- Docstring listed `res_color` instead of the actual parameter `pixel_color`.

#### Unused imports removed
- `main.py`: removed `pyautogui`, `win32api`, `win32con`, `random`, `keyboard`,
  `numpy`, and `pixel_check`.
- `utils/human_move.py`: removed unused `import time`.
- `utils/press_key.py`: removed unused `import random`.
- `gui/main_gui.py`: removed unused `import tkinter as tk`.

---

### Automated Test Suite (new in this PR)

#### `tests/conftest.py`
Shared pytest configuration that stubs out Windows-only modules (`win32api`,
`win32con`) so the suite runs cross-platform (macOS, Linux, CI) with no
display or Windows environment required.

#### `tests/test_finder.py` (165 lines, ~15 tests)
Unit tests for `utils/finder.py`:
- `locate_on_screen`: image-found, image-not-found, and exception paths.
- `pixel_check`: correct-color, wrong-color, and pyautogui-error paths.
- Random coordinate generation — verifies that produced `(x, y)` values stay
  strictly within the bounding box (validates the off-by-one fix).

#### `tests/test_human_move.py` (206 lines, ~15 tests)
Unit tests for `utils/human_move.py`:
- `human_move_curved`: validates Bézier-curve point generation, mouse movement
  calls, and timing behavior under various speed configurations.
- Edge cases: zero-distance moves, extreme control-point offsets.

#### `tests/test_main.py` (95 lines, ~10 tests)
Unit tests for the screen-location retry loop in `main.py`:
- Loop terminates when `locate_on_screen` returns a match.
- Loop continues and retries when the image is not found.
- `time.sleep` is called between retries.

#### `requirements.txt`
Added `pytest` as a development dependency.

---

## Files Modified

| File | Change |
|------|--------|
| `requirements.txt` | Added `pytest` |
| `tests/__init__.py` | New — makes `tests/` a package |
| `tests/conftest.py` | New — cross-platform stub for Windows modules |
| `tests/test_finder.py` | New — unit tests for `utils/finder.py` |
| `tests/test_human_move.py` | New — unit tests for `utils/human_move.py` |
| `tests/test_main.py` | New — unit tests for `main.py` retry loop |

*(Bug-fix files — `utils/finder.py`, `main.py`, `utils/human_move.py`,*
*`utils/press_key.py`, `gui/main_gui.py` — were modified in the prior PR.)*

---

## Follow-up Notes

- **Windows runtime testing**: Integration tests require a Windows host with a
  display; the current suite covers logic in isolation via mocks.
- **CI pipeline**: Consider adding a GitHub Actions workflow that runs
  `pytest tests/` on push to `dev` and `main`.
- **Retry safeguard**: `main.py` runs an infinite loop with no timeout or
  maximum-retry limit — adding one would improve robustness in production use.
- **Coverage**: Current tests exercise the happy path and key error paths;
  additional edge cases (e.g., `human_move_curved` with identical start/end
  points) can be added incrementally.
