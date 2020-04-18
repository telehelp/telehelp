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
    numArgs = len(sys.argv)  # TODO: Use argparse if complexity increased in future.
    if numArgs < 4:  # Print help message if not enough arguments
        helpStr = "This script sends an SMS broadcast to a numerically specified \
subgroup of registered volunteers in a provided district (län), according to this formula:\n\tsubgroup = user ID % numSubgroups\n\
\nUsage: \n\tpython sendSmsBroadcast.py <message> <district> <numSubgroups> <targetSubgroup> [<test phone numbers>]\n\
\nNote that you will need to confirm the broadcast manually before sending begins.\
\nNote that the <message> and <district> can be surrounded by single quotes to escape spaces.\
\nThe <district> can be specified as 'all' to broadcast to all districts at once.\
\nTo include formatted newlines in the <message>, use $'LINE1\\nLINE2'."
        print(helpStr)
    else:
        message = sys.argv[1]
        district = sys.argv[2]  # Swedish län
        numSubgroups = int(sys.argv[3])
        targetSubgroup = int(sys.argv[4])
        print(f"Message: {message}")
        print(f"Target district: {district}")
        print(f"Number of subgroups: {numSubgroups}")
        print(f"Target subgroup: {targetSubgroup}")

        if targetSubgroup >= numSubgroups:
            print(
                "ERROR: The target subgroup has to be less than the number of subgroups to split the userbase into."
            )
            return

        if numArgs > 5:  # Manually specified numbers, "trial run"
            targetNumbers = sys.argv[5:]
            print(f"Using manually specified targetNumbers: {targetNumbers}")
        else:
            if district == "all":
                query = """SELECT phone FROM user_helpers WHERE rowid%?==?"""
                query_params = (numSubgroups, targetSubgroup)
            else:
                query = """SELECT phone FROM user_helpers WHERE rowid%?==? AND district==?"""
                query_params = (numSubgroups, targetSubgroup, district)
            targetNumbersTuples = readDatabase(DATABASE, DATABASE_KEY, query, params=query_params)
            targetNumbers = [x[0] for x in targetNumbersTuples]
            print(f"The SMS broadcast will reach the following {len(targetNumbers)} users:")
            for num in targetNumbers:
                print(f" - {num}")

        confirmation = input("Continue? [y|n] ").lower()
        if confirmation == "y":
            performSmsBroadcast(message, targetNumbers)
        else:
            print("User aborted broadcast.")


def performSmsBroadcast(msg, numbers):
    totalNumbers = len(numbers)
    for numberIndex, number in enumerate(numbers):
        pattern = r"^\+46[0-9]{9}$"  # Pattern to match Swedish +46ddddddddd mobile phone number format (especially for manual input)
        if re.match(pattern, str(number)):

            requests.post(
                "https://api.46elks.com/a1/sms",
                auth=(API_USERNAME, API_PASSWORD),
                data={"from": "Telehelp", "to": number, "message": msg},
            )

            print(f"Sent message to user {numberIndex+1}/{totalNumbers}: {number}")
            time.sleep(0.5)  # Limit rate in case manual abort is necessary
        else:
            print(
                f"Skipping msg to user {numberIndex+1}/{totalNumbers}: {number} - does not match expected +46ddddddddd format..."
            )


if __name__ == "__main__":
    sendSmsBroadcast()
