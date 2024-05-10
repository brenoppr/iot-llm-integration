import pyautogui

print("Move the mouse to the desired position...")
try:
    while True:
        x, y = pyautogui.position()
        position_str = f"X: {x}, Y: {y}"
        print(position_str, end="\r")
except KeyboardInterrupt:
    print("\nCoordinates captured.")
