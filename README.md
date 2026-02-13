# WizBot

A Python automation toolkit featuring human-like mouse movements and image recognition for screen interaction.

## Features

- **Image Recognition** – Locate images on screen using template matching with configurable confidence levels
- **Human-like Mouse Movement** – Fitts' Law-based cursor movement with natural timing and optional curved paths
- **Pixel Detection** – Check specific pixel colors at any screen coordinate
- **Randomized Input** – Humanized key presses and clicks with variable delays
- **GUI Interface** – Simple CustomTkinter interface for testing image detection

## Requirements

- Python 3.10+
- Windows (uses `win32api` for mouse events)

## Installation

```bash
pip install pyautogui opencv-python customtkinter keyboard pywin32
```

## Project Structure

```
├── main.py              # Main entry point
├── gui/
│   └── main_gui.py      # CustomTkinter GUI
├── utils/
│   ├── finder.py        # Image location & pixel checking
│   ├── click.py         # Mouse click functions
│   ├── human_move.py    # Human-like cursor movement
│   ├── press_key.py     # Humanized keyboard input
│   ├── globals.py       # Random delay configurations
│   └── find_cur_pos.py  # Utility to display mouse position
└── images/              # Template images for detection
```

## Usage

### Basic Image Detection

```python
from utils.finder import locate_on_screen

# Finds image, moves cursor naturally, and clicks
if locate_on_screen("images/target.png", confidence=0.8):
    print("Found and clicked!")
```

### Human-like Mouse Movement

```python
from utils.human_move import human_move, human_move_curved

# Smooth movement with Fitts' Law timing
human_move(500, 300)

# Movement with subtle curve
human_move_curved(500, 300)
```

### Pixel Color Check

```python
from utils.finder import pixel_check

# Check if pixel at (100, 200) has red value of 255
if pixel_check(100, 200, 0, 255):
    print("Red pixel found!")
```

### GUI Mode

```bash
python -m gui.main_gui
```

## Configuration

Adjust timing parameters in `utils/globals.py`:

```python
def random_float():    # Click hold duration
    return random.uniform(0.08, 0.22)

def random_hold():     # Key hold duration
    return random.uniform(0.05, 0.12)

def random_delay():    # Delay between actions
    return random.uniform(0.05, 0.18)
```

## License

MIT
