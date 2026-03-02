# Smoke-Test Addition — Summary

## Changes Made

A basic smoke-test suite was added for the WizBot project.  All tests are
platform-agnostic: Windows-only packages (`win32api`, `win32con`, `keyboard`)
and display-dependent packages (`pyautogui`) are fully stubbed, so the suite
runs on Windows 11, macOS, and Linux with Python 3.9+.

---

## Files Added / Modified

| File | Action | Description |
|---|---|---|
| `conftest.py` | Added | Root-level pytest config. Stubs platform/display modules *before* any test module is collected. |
| `tests/__init__.py` | Added | Makes `tests/` a package. |
| `tests/test_globals.py` | Added | 6 smoke tests for `utils/globals.py` — checks each function returns a float in its expected range. |
| `tests/test_press_key.py` | Added | 7 smoke tests for `utils/press_key.py` — verifies importability and that `human_press` / `human_type` invoke `pyautogui` correctly. |
| `tests/test_main.py` | Added | 2 smoke tests for `main.py` — stubs `utils.finder.locate_on_screen` to `True` so the top-level while-loop exits on first iteration, then asserts the module loaded without error. |
| `requirements-test.txt` | Added | Single test dependency: `pytest>=7.4`. |

---

## How to Run the Tests

```bash
# 1. Install the single test dependency (no project packages required)
pip install -r requirements-test.txt

# 2. Run from the repo root
pytest tests/ -v
```

### Expected Output

```
collected 15 items

tests/test_globals.py::test_random_float_returns_float          PASSED
tests/test_globals.py::test_random_float_in_range               PASSED
tests/test_globals.py::test_random_hold_returns_float           PASSED
tests/test_globals.py::test_random_hold_in_range                PASSED
tests/test_globals.py::test_random_delay_returns_float          PASSED
tests/test_globals.py::test_random_delay_in_range               PASSED
tests/test_main.py::test_main_imports_without_error             PASSED
tests/test_main.py::test_main_calls_locate_on_screen            PASSED
tests/test_press_key.py::test_module_imports_without_error      PASSED
tests/test_press_key.py::test_human_press_is_callable           PASSED
tests/test_press_key.py::test_human_type_is_callable            PASSED
tests/test_press_key.py::test_human_press_calls_keydown_then_keyup  PASSED
tests/test_press_key.py::test_human_press_keydown_before_keyup  PASSED
tests/test_press_key.py::test_human_type_presses_each_character PASSED
tests/test_press_key.py::test_human_type_empty_sequence_does_nothing PASSED

15 passed in 0.01s
```

---

## Bugs Discovered (Not Fixed — Follow-Up Required)

### 1. `utils/globals.py` — `random_float()` has swapped arguments

```python
# Current (buggy):
return random.uniform(0.8, 0.22)   # 0.8 > 0.22 — args are in wrong order

# README documents the intent as:
return random.uniform(0.08, 0.22)  # likely a missing leading zero
```

Python does not raise an error when `a > b` in `random.uniform`, so this
silently produces values in `[0.22, 0.80]` instead of `[0.08, 0.22]`.  Click
hold durations will be ~4–10× longer than intended.

### 2. `utils/press_key.py` — `time.sleep` called with function objects

```python
# Current (buggy):
time.sleep(globals.random_hold)    # passes function object, not return value
time.sleep(globals.random_delay)   # same

# Should be:
time.sleep(globals.random_hold())
time.sleep(globals.random_delay())
```

At runtime this raises `TypeError: a float is required` on the first call to
`human_press`.  The bug is masked in tests because `time.sleep` is mocked.

---

## Follow-Up Notes

- Fix the two bugs listed above before using these modules in production.
- `main.py` executes a blocking while-loop at module scope.  Consider wrapping
  it in `if __name__ == "__main__":` to enable safe imports and better testability.
- The test suite does not cover `utils/finder.py`, `utils/click.py`,
  `utils/human_move.py`, or `gui/main_gui.py`.  These would benefit from
  additional unit tests, especially `_fitts_duration` in `human_move.py`
  which is pure math and needs no mocking.
- Consider adding a CI workflow (GitHub Actions) to run `pytest` automatically
  on each push.
