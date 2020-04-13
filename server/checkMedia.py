import os
import urllib.request


def checkURL(url):
    try:
        code = urllib.request.urlopen(url).getcode()
        return code
    except urllib.error.HTTPError as e:
        print(f"Warning can't find path: {url}. Status {e.code} {e.reason}")
        return e.code


def checkMedia(python_file, key_word):
    with open(python_file) as file:
        line = file.readline()
        if key_word in line and "checkMedia" not in line:
            pass


if __name__ == "__main__":
    print(checkURL("https://media.telehelp.se/sv/ivr/info.mp3"))
    checkMedia("api.py", "MEDIA_URL")
