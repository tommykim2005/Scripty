import pyautogui,time,random
from utils import globals

def human_press(key):
    """press a key with randomized delays

    Args:
        key (key): key
    """
    pyautogui.keyDown(key)
    time.sleep(globals.random_hold)
    pyautogui.keyUp(key)
    time.sleep(globals.random_delay)
    
def human_type(text):
    """type multiple keys with randomized delays

    Args:
        text (array): text 
    """
    for char in text:
        human_press(char)
    
    
    
