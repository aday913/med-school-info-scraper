import csv

import pyautogui as gui
import pyperclip as clip
import pyscreeze

EMAIL_IMAGE_PATH = "email.png"
LIGHT_ARROW_PATH = "light_arrow.png"
DARK_ARROW_PATH = "dark_arrow.png"
SPECIALTY_IMAGE_PATH = "specialty.png"
PROGRAM_NAME_IMAGE_PATH = "program_name.png"
ADDRESS_IMAGE_PATH = "address.png"


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


def get_arrow_locations():
    """
    This function will return all of the arrow locations on the screen

    :return: A list of tuples containing the x and y coordinates of the arrows
    """
    # Get all of the light and dark arrows on the screen
    try:
        light_arrows = gui.locateAllOnScreen(LIGHT_ARROW_PATH)
    except pyscreeze.ImageNotFoundException:
        light_arrows = []
        print("No light arrows found")

    try:
        dark_arrows = gui.locateAllOnScreen(DARK_ARROW_PATH)
    except pyscreeze.ImageNotFoundException:
        dark_arrows = []
        print("No dark arrows found")

    arrow_locations = []
    for i in light_arrows:
        arrow_locations.append(i)
    for i in dark_arrows:
        arrow_locations.append(i)

    print(f"Found {len(arrow_locations)} arrows on screen")
    return arrow_locations


def save_to_csv(processed_programs: dict, output_name: str):
    with open(output_name, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Program Name", "Email", "Specialty", "Address"])
        for program_name, info in processed_programs.items():
            writer.writerow(
                [program_name, info["email"], info["specialty"], info["address"]]
            )


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

    OVERVIEW_PROGRAM_NAME_OFFSET = 200
    OVERVIEW_PROGRAM_NAME_WIDTH = 300
    OVERVIEW_PROGRAM_NAME_HEIGHT = 40

    ADDRESS_OFFSET = 200
    ADDRESS_WIDTH = 300
    ADDRESS_HEIGHT = 40

    # Keep track of which programs we've processed:
    processed_programs = {}

    previous_arrow_locations = []
    while True:
        try:
            # First find all of the arrows on the screen
            arrow_locations = []
            previous_arrow_locations = []
            scrolled_already = False
            while arrow_locations == []:
                print("Attempting to get all arrow locations on screen")
                arrow_locations = get_arrow_locations()
                if arrow_locations == []:
                    print("No arrows found, press enter when you have arrows on screen")
                    input()

                if arrow_locations == previous_arrow_locations and not scrolled_already:
                    # We want to scroll down in this case
                    print("No new arrows found, scrolling down")
                    gui.scroll(-1000)
                    scrolled_already = True
                elif arrow_locations == previous_arrow_locations and scrolled_already:
                    print(
                        "No new arrows found, press enter when you have new arrows on screen"
                    )
                    input()
            previous_arrow_locations = arrow_locations

            # Loop through all of the arrows
            for arrow in arrow_locations:
                print("--------------------------------------------")
                # Get the program name
                program_name = get_text_info(
                    arrow.left + (0.5 * int(arrow.width)),
                    arrow.top + (0.5 * int(arrow.height)),
                    OVERVIEW_PROGRAM_NAME_OFFSET,
                    OVERVIEW_PROGRAM_NAME_WIDTH,
                    OVERVIEW_PROGRAM_NAME_HEIGHT,
                )
                print(f"Found program name {program_name}")
                if program_name in list(processed_programs.keys()):
                    print(f"Already processed {program_name}, skipping")
                    continue
                processed_programs[program_name] = {
                    "email": None,
                    "specialty": None,
                    "address": None,
                }

                # Click on the link
                gui.click(
                    (
                        arrow.left + (0.5 * int(arrow.width)) + 100
                    ),  # 100 to the right of the arrow
                    (arrow.top + (0.5 * int(arrow.height))),
                )

                # Now we're in the program details page

                # Get the email
                try:
                    email_location = gui.locateOnScreen(EMAIL_IMAGE_PATH)
                except pyscreeze.ImageNotFoundException:
                    print(f"No email found for {program_name}")
                else:
                    email = get_text_info(
                        email_location.left + (0.5 * float(email_location.width)),
                        email_location.top + (0.5 * float(email_location.height)),
                        EMAIL_OFFSET,
                        EMAIL_WIDTH,
                        EMAIL_HEIGHT,
                    )
                    print(f"Found email {email}")
                    processed_programs[program_name]["email"] = email

                # Get the specialty
                try:
                    specialty_location = gui.locateOnScreen(SPECIALTY_IMAGE_PATH)
                except pyscreeze.ImageNotFoundException:
                    print(f"No specialty found for {program_name}")
                else:
                    specialty = get_text_info(
                        specialty_location.left
                        + (0.5 * float(specialty_location.width)),
                        specialty_location.top
                        + (0.5 * float(specialty_location.height)),
                        SPECIALTY_OFFSET,
                        SPECIALTY_WIDTH,
                        SPECIALTY_HEIGHT,
                    )
                    print(f"Found specialty {specialty}")
                    processed_programs[program_name]["specialty"] = specialty

                # Get the address
                try:
                    address_location = gui.locateOnScreen(ADDRESS_IMAGE_PATH)
                except pyscreeze.ImageNotFoundException:
                    print(f"No address found for {program_name}")
                else:
                    address = get_text_info(
                        address_location.left + (0.5 * float(address_location.width)),
                        address_location.top + (0.5 * float(address_location.height)),
                        ADDRESS_OFFSET,
                        ADDRESS_WIDTH,
                        ADDRESS_HEIGHT,
                    )
                    print(f"Found address {address}")
                    processed_programs[program_name]["address"] = address

                # Click on the "x" to go back to the overview page
                x_location = gui.locateOnScreen("x.png")
                gui.click(
                    x_location.left + (0.5 * float(x_location.width)),
                    x_location.top + (0.5 * float(x_location.height)),
                )
        except KeyboardInterrupt:
            print("Exiting and saving to output.csv")
            save_to_csv(processed_programs, "output.csv")
            break


if __name__ == "__main__":
    main()
