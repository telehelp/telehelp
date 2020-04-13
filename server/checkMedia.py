import json
import os
import re
import urllib.request


def checkURL(url, log=None):
    try:
        code = urllib.request.urlopen(url).getcode()
        # print("Path found")
        return code
    except urllib.error.HTTPError as e:
        print(f"Warning can't find path: {url}. Status {e.code} {e.reason}")
        if log is not None:
            log.warning(f"Can't find path: {url}. Status {e.code} {e.reason}")
        return e.code


def checkPayload(payload, key_word, log=None):
    for key in payload.keys():
        if isinstance(payload[key], str):
            # print(payload[key])
            if key_word in payload[key]:
                checkURL(payload[key])
        elif isinstance(payload[key], dict):
            checkPayload(payload[key], key_word)


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
                "ivr": MEDIA_URL + "/ivr/stamme_det.mp3",
                "1": BASE_URL + f"/postcodeInput/{zipcode}",
                "2": BASE_URL + "/handleNumberInput",
                "next": BASE_URL + "/handleNumberInput",
            },
        },
    }
    checkPayload(payload, MEDIA_URL)
