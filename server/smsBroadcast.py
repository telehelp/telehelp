import os
import re
import sys
import time

import requests
from dotenv import load_dotenv

from .databaseIntegration import readDatabase

load_dotenv()

# Set API_USERNAME, API_PASSWORD
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")

# ACCESS TO DATABASE
DATABASE = os.getenv("DATABASE")
DATABASE_KEY = os.getenv("DATABASE_KEY")


def sendSmsBroadcast():
    numArgs = len(sys.argv)
    if numArgs < 4:  # Print help message if not enough arguments
        helpStr = "This script sends an SMS broadcast to a numerically specified subgroup of registered volunteers: \
subgroup = user ID % numSubgroups\nNote that you will need to confirm the message sending manually.\
\nUsage: python sendSmsBroadcast.py <message> <numSubgroups> <targetSubgroup> [<test phone numbers>]\
\nNote that the <message> should be surrounded by single quotes to escape spaces."
        print(helpStr)
    else:
        message = sys.argv[1]
        numSubgroups = int(sys.argv[2])
        targetSubgroup = int(sys.argv[3])
        print(f"Message: {message}")
        print(f"Number of subgroups: {numSubgroups}")
        print(f"Target subgroup: {targetSubgroup}")

        if targetSubgroup >= numSubgroups:
            print(
                "ERROR: The target subgroup has to be less than the number of subgroups to split the userbase into."
            )
            return

        query = """SELECT phone FROM user_helpers WHERE rowid%?==?"""
        targetNumbersTuples = readDatabase(
            DATABASE, DATABASE_KEY, query, params=(numSubgroups, targetSubgroup)
        )
        targetNumbers = [x[0] for x in targetNumbersTuples]

        print(f"The SMS broadcast will reach the following {len(targetNumbers)} users:")
        for num in targetNumbers:
            print(f" - {num}")
        if numArgs > 4:  # Trial run
            targetNumbers = sys.argv[4:]
            print(f"THIS IS JUST A TEST RUN, overriding targetNumbers with: {targetNumbers}")
        confirmation = input("Continue? [y|n] ").lower()
        if confirmation == "y":
            performSmsBroadcast(message, targetNumbers)
        else:
            print("User aborted broadcast.")


def performSmsBroadcast(msg, numbers):
    totalNumbers = len(numbers)
    for numberIndex in range(totalNumbers):
        number = numbers[numberIndex]

        pattern = r"^\+46[0-9]{9}$"  # Pattern to match Swedish +46ddddddddd mobile phone number format
        if re.match(pattern, str(number)):

            requests.post(
                "https://api.46elks.com/a1/sms",
                auth=(API_USERNAME, API_PASSWORD),
                data={"from": "Telehelp", "to": number, "message": msg},
            )

            print(f"Sent message to user {numberIndex+1}/{totalNumbers}: {number}")
            time.sleep(1)  # Max rate for the 46elks API is 100 SMS per minute.
        else:
            print(
                f"Skipping msg to user {numberIndex+1}/{totalNumbers}: {number} - does not match expected +46ddddddddd format..."
            )


if __name__ == "__main__":
    sendSmsBroadcast()
