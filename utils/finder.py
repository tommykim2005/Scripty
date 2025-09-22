import pyautogui,random
from utils import click
from utils.human_move import human_move,human_move_curved


def locate_on_screen(image_path, confidence = 0.8):
    try:
        box = pyautogui.locateOnScreen(image_path,grayscale=True, confidence=confidence)
        if not box:
            print("Image not Found")
            return False
        x = random.randint(box.left,box.left + box.width)
        y = random.randint(box.top,box.top+box.height)
        human_move_curved(x,y)
        click.click(x,y)
        print(f"Clicked at ({x}, {y})")
        return True
    except pyautogui.ImageNotFoundException:
        print("PyAutoGUI could not find the image (exception)")
        return False

def pixel_check(x,y,color,pixel_color):
    """check if pixel at x,y is a certain color

    Args:
        x (int): x coord
        y (int): y coord
        color (int): 0 = red, 1 = green, 2 = blue
        res_color (int): r,g,b value for chosen pixel

    Returns:
        _type_: _description_
    """
    if pyautogui.pixel(x,y)[color] != pixel_color:
        return False
    else:
        return True