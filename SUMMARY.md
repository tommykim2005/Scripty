# Setup Summary – WizBot (scripty)

## Repository

- **Remote:** `https://github.com/tommykim2005/scripty`
- **Branch:** `agent/scripty/feat/initial-setup`
- **Cloned to:** current working directory (already present on disk)

---

## Changes Made

### Files Created

| File | Description |
|---|---|
| `requirements.txt` | Pinned dependency list with platform guard for `pywin32` |
| `SETUP.md` | Step-by-step setup guide (prerequisites, install, run, config) |
| `SUMMARY.md` | This file |

### Files Modified

None — existing source files were not altered.

---

## Dependency Installation

All cross-platform packages installed successfully via `pip install -r requirements.txt`:

| Package | Version installed |
|---|---|
| PyAutoGUI | 0.9.54 |
| opencv-python | 4.13.0.92 |
| customtkinter | 5.2.2 |
| keyboard | 0.13.5 |
| numpy | 2.0.2 |
| pywin32 | skipped (macOS) |

---

## Build / Runtime Verification

Verification was run on **macOS (Darwin 24.3.0), Python 3.9.6**.

| Module | Result | Reason |
|---|---|---|
| `utils.globals` | PASS | Pure Python, no platform deps |
| `utils.press_key` | PASS | Imports only pyautogui + globals |
| `utils.human_move` | FAIL | `float \| None` syntax requires Python 3.10+ (PEP 604) |
| `utils.click` | FAIL | Requires `win32api` (Windows only) |
| `utils.finder` | FAIL | Cascades from `utils.click` failure |

All eight source files pass `ast.parse()` (no syntax errors).

---

## Follow-up Notes

### Platform Constraint
The project is **Windows-only**. `utils/click.py` imports `win32api` and `win32con`
(from `pywin32`), which are not available on macOS or Linux. Full execution requires
a Windows 10/11 host.

### Python Version Constraint
`utils/human_move.py` uses `float | None` union-type annotations (PEP 604),
which require **Python 3.10 or later**. Running on Python 3.9 raises
`TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`
at import time.

### Bugs Identified (not fixed — see SETUP.md for details)

1. **`utils/globals.py:6`** – `random.uniform(0.8, 0.22)` has min > max; effective
   range is 0.22–0.80 instead of the documented 0.08–0.22.

2. **`utils/press_key.py:11,13`** – `globals.random_hold` and `globals.random_delay`
   are referenced as bare names (no `()`), passing function objects where float
   delays are expected; `time.sleep()` will raise `TypeError` at runtime.

### No Environment Variables Required
The project has no `.env`, config files, or secrets. All tuning is done directly
in `utils/globals.py`.

### Recommended Next Steps
- Run on a **Windows machine with Python 3.10+** for full functionality.
- Add `images/coin.png` (or another target image) before running `main.py`.
- Fix the two bugs listed above before deploying.
