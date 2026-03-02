# Setup Summary

**Date:** 2026-03-01
**Branch:** `agent/scripty/feat/initial-setup`
**Project:** WizBot – Python automation toolkit (human-like mouse/keyboard input + image recognition)

---

## Changes Made

| File | Action |
|------|--------|
| `requirements.txt` | Created – codifies all dependencies from README |

---

## Setup Steps Performed

### 1. Repository
The repository was already present in the working directory (no clone needed).
Checked out branch: `agent/scripty/feat/initial-setup`.

### 2. Dependencies Installed

All cross-platform packages were already installed (confirmed via `pip3 list`):

| Package | Version | Notes |
|---------|---------|-------|
| pyautogui | 0.9.54 | OK |
| opencv-python | 4.13.0 | OK |
| customtkinter | 5.2.2 | OK |
| keyboard | 0.13.5 | OK (no `__version__` attr, but imports correctly) |
| numpy | 2.0.2 | OK |
| Pillow | 11.3.0 | OK |
| **pywin32** | — | **Not available on macOS** (Windows-only; install on Windows targets only) |

Install command for a Windows target:
```
pip install -r requirements.txt
```

### 3. Environment Variables
None required. The project uses no `os.environ` / `.env` configuration.

### 4. Build / Import Verification

Run on macOS (darwin), Python 3.9.6.

| Module | Status | Detail |
|--------|--------|--------|
| `pyautogui` | Pass | |
| `opencv-python` (cv2) | Pass | |
| `customtkinter` | Pass | |
| `keyboard` | Pass | |
| `numpy` | Pass | |
| `Pillow` | Pass | |
| `win32api` / `win32con` | **Fail** | Windows-only; expected on macOS |
| `utils.globals` | Pass | `random_delay()` returns correct float |
| `utils.human_move` | **Fail** | `float \| None` union syntax requires Python 3.10+; current env is 3.9.6 |
| `utils.click` | **Fail** | Imports `win32api` – Windows-only |
| `utils.finder` | **Fail** | Transitively imports `utils.click` (win32api) |
| `gui.main_gui` | **Fail** | Transitively imports `utils.finder` |
| `main.py` | **Fail** | Imports `win32api` directly |

---

## Issues Found

### Issue 1 – Windows-only dependency (`pywin32`)
`utils/click.py` and `main.py` import `win32api` / `win32con`, which are only available on Windows.
**Impact:** The project will not run on macOS or Linux.
**Resolution:** Run on a Windows 11 host as documented in the README. `pywin32` installs normally on Windows via `pip install pywin32`.

### Issue 2 – Python 3.10+ type union syntax in `utils/human_move.py`
Lines 14 and 34 use `float | None` (PEP 604 union type hints), which requires Python 3.10+:
```python
def human_move(x: int, y: int, duration: float | None = None, ...):
```
**Impact:** Module fails to import on Python 3.9.
**Resolution (two options):**
- **Preferred:** Upgrade the runtime to Python 3.10+.
- **Quick fix:** Replace `float | None` with `Optional[float]` and add `from typing import Optional` at the top of `utils/human_move.py`.

### Issue 3 – Bug in `utils/globals.py` `random_float()`
```python
def random_float():
    return random.uniform(0.8, 0.22)   # min > max – always returns 0.22
```
The lower bound (`0.8`) is larger than the upper bound (`0.22`). `random.uniform` will always return `0.22` in this state.
**Resolution:** Fix the bounds – likely intended to be `random.uniform(0.08, 0.22)` (matching the README).

### Issue 4 – `utils/press_key.py` calls globals without parentheses
```python
time.sleep(globals.random_hold)   # missing ()
time.sleep(globals.random_delay)  # missing ()
```
Both are references to the function object, not a call. `time.sleep` will raise `TypeError` at runtime.
**Resolution:** Add parentheses: `globals.random_hold()` and `globals.random_delay()`.

---

## Follow-up Notes

1. **Target platform:** Deploy and run on Windows 11 (as described in `AGENTS.md`).
2. **Python version:** Ensure Windows target runs Python 3.10+ to support the `float | None` syntax.
3. **Bug fixes recommended** (Issues 3 & 4 above) before using `utils/globals.py` and `utils/press_key.py` in production.
4. **Images directory:** `images/` is empty. Populate with template `.png` files before running `main.py` or the GUI.
5. **No tests exist** in the project. Consider adding basic smoke tests.
