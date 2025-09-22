import win32api,win32con,time
from utils import globals

def click(x,y):
    """Click at x,y 

    Args:
        x (int): x coord
        y (int): y coord
    """
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0,0)
    time.sleep(globals.random_float());
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0,0)
