import csv

import pyautogui as gui
import pyperclip as clip

EMAIL_IMAGE_PATH = "email.png"
LIGHT_ARROW_PATH = "light_arrow.png"
DARK_ARROW_PATH = "dark_arrow.png"
SPECIALTY_IMAGE_PATH = "specialty.png"
PROGRAM_NAME_IMAGE_PATH = "program_name.png"
ADDRESS_IMAGE_PATH = "address.png"


def get_image_location(path: str):
    return gui.locateOnScreen(path)


def get_text_info(
    initial_x: int, initial_y: int, x_offset: int, width: int, height: int
) -> str:
    """
    Given an initial position, an x offset, and a width, this function will
    select the text and copy it to the clipboard

    :param initial_x: The initial x position to start from
    :param initial_y: The initial y position to start from
    :param x_offset: The x offset to move from the initial position
    :param width: The width of the text
    :param height: The height of the text

    :return: The copied text
    """
    # Move to the initial position
    gui.moveTo(initial_x, initial_y)

    # Move over to the start of the text
    gui.move(x_offset, 0)

    # Select the text
    gui.dragRel(width, height, duration=0.5)

    # Copy the text to the clipboard
    gui.hotkey("ctrl", "c")

    # Return the copied text
    return clip.paste()




def main():
    # define offset, width, and height variables for all info fields

    EMAIL_OFFSET = 222
    EMAIL_WIDTH = 300
    EMAIL_HEIGHT = 0

    SPECIALTY_OFFSET = 210
    SPECIALTY_WIDTH = 200
    SPECIALTY_HEIGHT = 0

    PROGRAM_NAME_OFFSET = 185
    PROGRAM_NAME_WIDTH = 430
    PROGRAM_NAME_HEIGHT = 0

    ADDRESS_OFFSET = 200
    ADDRESS_WIDTH = 300
    ADDRESS_HEIGHT = 40

    # First find all of the arrows on the screen
    light_arrow = get_image_location(LIGHT_ARROW_PATH)
    print(light_arrow)
    dark_arrow = get_image_location(DARK_ARROW_PATH)


if __name__ == "__main__":
    main()
