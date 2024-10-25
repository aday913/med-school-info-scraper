import pyautogui as gui

while True:
    try:
        print(f"Mouse location: {gui.position()}")
    except KeyboardInterrupt:
        break
