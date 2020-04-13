import os
import re
import urllib.request


def checkURL(url):
    try:
        code = urllib.request.urlopen(url).getcode()
        return code
    except urllib.error.HTTPError as e:
        print(f"Warning can't find path: {url}. Status {e.code} {e.reason}")
        return e.code


def parseFString(fstring):
    print(fstring)
    pattern = re.compile(r"f{1}(\".+\")|(\'.+\')")
    print(pattern.search(fstring))
    # print(checkURL(fstring))


def checkMedia(python_file, key_word):
    with open(python_file) as file:
        line = file.readline()
        if key_word in line and "checkMedia" not in line:
            if "f" not in line:
                print(f"Warning! detected key_word that is not included in an fstring")
            else:
                pass


if __name__ == "__main__":
    MEDIA_URL = "https://files.telehelp.se/sv"
    # print(checkURL("https://media.telehelp.se/sv/ivr/info.mp3"))
    parseFString('                "ivr": f"{MEDIA_URL}/ivr/hjalper_ingen.mp3",')
    checkMedia("api.py", "MEDIA_URL")
