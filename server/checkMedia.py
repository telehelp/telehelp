import json
import os
import re
import urllib.request


def checkURL(url):
    try:
        code = urllib.request.urlopen(url).getcode()
        # print("Path found")
        return code
    except urllib.error.HTTPError as e:
        print(f"Warning can't find path: {url}. Status {e.code} {e.reason}")
        return e.code


def checkPayload(payload, key_word):
    for key in payload.keys():
        if isinstance(payload[key], str):
            print(payload[key])
            if key_word in payload[key]:
                checkURL(payload[key])
        elif isinstance(payload[key], dict):
            checkPayload(payload[key], key_word)


def parseLine(line):
    print(line)
    pattern = re.compile(r"f{1}(\".+\")|(\'.+\')")
    fString = pattern.search(line)
    if fString is not None:
        print(fString)

    # print(checkURL(fstring))


def checkMedia(python_file, key_word):
    row = 0
    with open(python_file) as file:
        line = file.readline()
        if key_word in line and "checkMedia" not in line:
            if "f" not in line:
                print(
                    f"Warning! detected key_word that is not included in an fstring on row: {row}. Can't check that path"
                )
            else:
                pass
        row += 1


if __name__ == "__main__":
    MEDIA_URL = "https://files.telehelp.se/sv"
    BASE_URL = "https://telehelp.se"
    # print(checkURL("https://media.telehelp.se/sv/ivr/info.mp3"))
    # parseLine('                "ivr": f"{MEDIA_URL}/ivr/hjalper_ingen.mp3",')
    # checkMedia("api.py", "MEDIA_URL")
    city = "Solna"
    cityEncoded = urllib.parse.quote(city)
    zipcode = "17070"
    payload = {
        "play": f"{MEDIA_URL}/ivr/du_befinner.mp3",
        "next": {
            "play": f"{MEDIA_URL}/city/{cityEncoded}.mp3",
            "next": {
                "ivr": MEDIA_URL + "/ivr/stammer_det.mp3",
                "1": BASE_URL + f"/postcodeInput/{zipcode}",
                "2": BASE_URL + "/handleNumberInput",
                "next": BASE_URL + "/handleNumberInput",
            },
        },
    }
    checkPayload(payload, MEDIA_URL)
