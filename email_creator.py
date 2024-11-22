import csv
import os
import time

from dotenv import load_dotenv
from openai import OpenAI
import pyautogui as gui
import pyperclip as clip
import pyscreeze

COMPOSE_BUTTON = (70, 70)  # (x, y) coordinates of the compose button
TO_FIELD = (200, 200)  # (x, y) coordinates of the "To" field
SUBJECT_FIELD = (200, 300)  # (x, y) coordinates of the subject field
BODY_FIELD = (200, 400)  # (x, y) coordinates of the body field

CSV_FILE = "emails.csv"


def read_csv(file_path: str) -> list:
    """
    Read a CSV file and return the data as a list of lists

    :param file_path: The path to the CSV file

    :return: A list of lists, where each inner list is a row from the CSV file
    """
    return_data = []
    print(f"Reading CSV file: {file_path}")

    # Read the CSV file
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:

            # Skip empty rows
            for i in row:
                if i.strip():
                    break
            else:
                continue

            # Append the row to the return data
            return_data.append([i.strip() for i in row])

    # Print some information about the CSV file
    print(f"Read {len(return_data)} rows from the CSV file")
    print(f"First 5 rows: {return_data[:5]}")

    return return_data


def main(openai: OpenAI, model: str):

    # General flow:
    # 1. Read the CSV file with emails, program names, specialties, and address

    print("Reading the CSV file")
    data = read_csv(CSV_FILE)

    # 2. For each row in the CSV file, generate an OpenAI prompt
    for row in data:
        rerun = True
        while rerun:
            print("=====================================")
            name, email, specialty, address = row

            # 2a. Ask the user if we should even generate an email, as they may have already
            should_continue: str = ""
            while should_continue.strip().lower() not in ("y", "n"):
                should_continue = input(
                    f"Should we generate an email for {name}'s {specialty} program? (y/n): "
                )

            if should_continue.lower() == "n":
                continue

            prompt = f"""
                    Please write me a letter of interest for the {specialty} program at {name} that I can send to the 
                    program director. The address of this location, to the best of my knowledge, is {address}.

                    Please also include the fact that I updated my personal statement on the ERAS application, 
                    as I previously selected the wrong personal statement. The new personal statement is now uploaded.

                """

            additional_input = input(
                "Is there any additional information you would like to provide for the email? Type it out here and press enter: "
            )
            prompt += additional_input

            print("Prompt generated:\n")
            print(prompt + "\n")

            # 4. Send the prompt to OpenAI and get the response
            setup = """
                You are an expert at crafting letter of interest emails that will be sent to medical residency 
                program directors to cause them to consider a given person's application. 
                Your response should only include the email body itself, with no meta information 
                regarding the generation of the text, clarifications, etc. 
                The email should be professional, concise, and persuasive, using a template similar to that
                found at the link https://www.mominsamad.com/residency-letter-of-interest-template/, but not following
                that template exactly. The email should be tailored to the specific program. Please think about the
                program's strengths and unique opportunities (which I will not provide). 
            """

            print("Sending prompt to OpenAI...")
            completion = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": setup},
                    {"role": "user", "content": prompt},
                ],
            )
            response = completion.choices[0].message.content

            # If there's no response, try again
            if not response:
                print("No response generated. Please try again.")
                continue

            print("Response generated:\n")
            print(response + "\n")

            # 5. Click the "compose" button in gmail and wait 2 seconds
            print("Clicking the compose button")
            gui.click(COMPOSE_BUTTON)
            time.sleep(2)

            # 6. Click the "To" field and paste the email address
            print("Clicking the 'To' field")
            gui.click(TO_FIELD)
            clip.copy(email)
            gui.hotkey("ctrl", "v")
            time.sleep(1)

            # 7. Click the "Subject" field and paste the subject
            print("Clicking the 'Subject' field")
            gui.click(SUBJECT_FIELD)
            clip.copy(f"Letter of Interest for {specialty} Program at {name}")
            gui.hotkey("ctrl", "v")
            time.sleep(1)

            # 8. Click the "Body" field and paste the OpenAI response
            print("Clicking the 'Body' field")
            gui.click(BODY_FIELD)
            clip.copy(response)
            gui.hotkey("ctrl", "v")
            time.sleep(1)

            # 9. Ask the user to confirm the email and click send
            should_rerun = ''
            while should_rerun.strip().lower() not in ('y', 'n'):
                should_rerun = input("Do you want to re-generate the email? Saying no moves on to the next program. Be sure to send the email! (y/n): ")
            if should_rerun.strip().lower() == 'n':
                rerun = False



if __name__ == "__main__":
    load_dotenv()

    API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    if API_KEY is None:
        raise ValueError("API_KEY is not set")

    openai = OpenAI(api_key=API_KEY)
    model = "gpt-4o"

    main(openai, model)
