import pyautogui
import time
def click(x,y):
# Get the screen resolution
    screen_width, screen_height = pyautogui.size()

# Define the position where you want to click (x, y coordinates)
    click_x = x
    click_y = y
    
# Move the mouse to the desired position and click
    pyautogui.click(click_x, click_y)

