# Bug Fix Summary

## Changes Made

### 1. `utils/finder.py` — Off-by-one in random click coordinate selection
- **Bug:** `random.randint(box.left, box.left + box.width)` and `random.randint(box.top, box.top + box.height)` could generate coordinates one pixel outside the right/bottom edge of the matched image region. `pyautogui`'s `Box` namedtuple uses `(left, top, width, height)`, so valid x values are `box.left` through `box.left + box.width - 1` (inclusive).
- **Fix:** Changed to `random.randint(box.left, box.left + box.width - 1)` and `random.randint(box.top, box.top + box.height - 1)`.

### 2. `utils/finder.py` — Docstring parameter name mismatch in `pixel_check`
- **Bug:** The docstring listed `res_color` as the fourth parameter name, but the actual parameter is `pixel_color`.
- **Fix:** Updated docstring to use `pixel_color`.

### 3. `main.py` — Unused imports
- **Bug:** `pyautogui`, `win32api`, `win32con`, `random`, `keyboard`, and `numpy` were all imported but never referenced in `main.py`. Additionally `pixel_check` was imported from `utils.finder` but never called.
- **Fix:** Removed all unused imports; kept only `time` (used in `time.sleep`) and `locate_on_screen` (used in the while loop).

### 4. `utils/human_move.py` — Unused `import time`
- **Bug:** `import time` was present but `time` was never used in the module.
- **Fix:** Removed the unused import.

### 5. `utils/press_key.py` — Unused `import random`
- **Bug:** `import random` was present but `random` was never used directly in the module (randomization is handled via `globals`).
- **Fix:** Removed the unused import.

### 6. `gui/main_gui.py` — Unused `import tkinter as tk`
- **Bug:** `import tkinter as tk` was present but `tk` was never referenced; the GUI uses `customtkinter` exclusively.
- **Fix:** Removed the unused import.

## Files Modified

| File | Change |
|------|--------|
| `utils/finder.py` | Off-by-one fix: `box.width` → `box.width - 1`, `box.height` → `box.height - 1`; docstring `res_color` → `pixel_color` |
| `main.py` | Removed unused imports: `pyautogui`, `win32api`, `win32con`, `random`, `keyboard`, `numpy`, `pixel_check` |
| `utils/human_move.py` | Removed unused `import time` |
| `utils/press_key.py` | Removed unused `import random` |
| `gui/main_gui.py` | Removed unused `import tkinter as tk` |

## Testing

Static analysis was performed on all Python files. Runtime testing is not possible in this environment because the project targets Windows (requires `win32api` and a display server). The fixes are verified by inspection:

- The off-by-one fix ensures `random.randint` upper bounds stay within the image box boundaries.
- All removed imports were confirmed to have zero references in their respective files.
- The docstring fix aligns documentation with the actual parameter name.

## Follow-up Notes

- Integration testing should be done on Windows with a running display to validate the full automation pipeline (`locate_on_screen` → `human_move_curved` → `click`).
- `main.py` runs an infinite loop until the coin image is found with no timeout or maximum-retry limit — consider adding a safeguard for production use.
- The project has no automated tests; adding a test suite (e.g., with `pytest` and mocked `pyautogui`) would help catch regressions.
