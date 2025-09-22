import pyautogui,win32api,win32con,random,keyboard,time
import numpy as np
from utils.finder import locate_on_screen, pixel_check


while not locate_on_screen("images/coin.png"):
    print("Could not locate retrying")
    time.sleep(.5)
print("Success")
