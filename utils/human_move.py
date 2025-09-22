# utils/human_move.py
import pyautogui
import time
import random
import math

def _fitts_duration(distance_px: float, target_width_px: float = 40.0,
                    a: float = 0.12, b: float = 0.085) -> float:
    """Rough human-like timing (seconds) via Fitts' Law."""
    distance_px = max(distance_px, 1.0)
    target_width_px = max(target_width_px, 4.0)
    return a + b * math.log2(distance_px / target_width_px + 1.0)

def human_move(x: int, y: int, duration: float | None = None,
               target_width_px: float = 40.0,
               easing=pyautogui.easeInOutQuad):
    """
    Smooth, human-like move with NO mini-stops.
    Relies on PyAutoGUI's built-in tweening to interpolate the path.
    """
    sx, sy = pyautogui.position()
    dist = math.hypot(x - sx, y - sy)

    # If caller didn't specify duration, pick one that feels human.
    if duration is None:
        duration = _fitts_duration(dist, target_width_px)
        # add slight randomness so it doesn't look identical every time
        duration *= random.uniform(0.9, 1.15)

    # Glide smoothly to the point with easing (no per-step sleeps).
    pyautogui.moveTo(x, y, duration=duration, tween=easing)

# OPTIONAL: curved variant if you want a gentle “arc” sometimes.
def human_move_curved(x: int, y: int, duration: float | None = None,
                      target_width_px: float = 40.0,
                      easing=pyautogui.easeInOutQuad):
    """
    Adds a subtle curve by inserting one midpoint, but still lets
    PyAutoGUI tween between the segments (minimal stops).
    """
    sx, sy = pyautogui.position()
    dist = math.hypot(x - sx, y - sy)
    if duration is None:
        duration = _fitts_duration(dist, target_width_px) * random.uniform(0.95, 1.1)

    # Midpoint offset to create a light curve
    mx = (sx + x) / 2 + random.randint(-60, 60)
    my = (sy + y) / 2 + random.randint(-60, 60)

    # Split duration across segments (keeps it smooth)
    d1 = duration * random.uniform(0.45, 0.6)
    d2 = max(0.05, duration - d1)

    pyautogui.moveTo(int(mx), int(my), duration=d1, tween=easing)
    pyautogui.moveTo(int(x),  int(y),  duration=d2, tween=easing)