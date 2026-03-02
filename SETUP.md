# WizBot – Setup Guide

## Prerequisites

| Requirement | Details |
|---|---|
| **OS** | Windows 10 / 11 only (`win32api` is Windows-exclusive) |
| **Python** | 3.10 or later (uses `X \| Y` union-type syntax from PEP 604) |
| **pip** | 21+ recommended |

## 1. Clone the Repository

```bash
git clone https://github.com/tommykim2005/scripty
cd scripty
```

## 2. (Optional) Create a Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:

| Package | Purpose |
|---|---|
| `pyautogui` | Screen capture, mouse/keyboard control |
| `opencv-python` | Template image matching |
| `customtkinter` | GUI interface |
| `keyboard` | Global key-press events |
| `pywin32` | Low-level Windows mouse events (Windows only) |
| `numpy` | Array operations used by OpenCV |

> **Note:** `pywin32` is automatically skipped on non-Windows platforms.

## 4. Add Template Images

Place any PNG images you want to match on screen inside the `images/` directory.
The default entry point (`main.py`) looks for `images/coin.png`.

```
images/
└── coin.png   ← required for main.py to run
```

## 5. Run the Project

### Console mode (image-detection loop)
```bash
python main.py
```

### GUI mode (CustomTkinter interface)
```bash
python -m gui.main_gui
```

### Cursor-position utility
```bash
python utils/find_cur_pos.py
```

## 6. Configuration

Timing randomisation is controlled in `utils/globals.py`:

```python
def random_float():   # Mouse-button hold duration (seconds)
    return random.uniform(0.08, 0.22)

def random_hold():    # Key hold duration (seconds)
    return random.uniform(0.05, 0.12)

def random_delay():   # Delay between actions (seconds)
    return random.uniform(0.05, 0.18)
```

No environment variables or external configuration files are required.

## Known Issues

| File | Issue |
|---|---|
| `utils/globals.py:6` | `random.uniform(0.8, 0.22)` – min > max (should be `0.08`); Python silently swaps values, producing a range of ~0.22–0.80 instead of 0.08–0.22 |
| `utils/press_key.py:11,13` | `globals.random_hold` and `globals.random_delay` are referenced without `()`, so they receive the function objects rather than float values |
| `utils/human_move.py` | `float \| None` union syntax requires Python 3.10+; causes `TypeError` on Python 3.9 |
| `utils/click.py` | Imports `win32api`/`win32con` which are unavailable outside Windows |
