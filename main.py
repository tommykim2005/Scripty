import time
from utils.finder import locate_on_screen


while not locate_on_screen("images/coin.png"):
    print("Could not locate retrying")
    time.sleep(.5)
print("Success")
