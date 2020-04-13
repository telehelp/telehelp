import os


def checkMedia(python_file, key_word):
    with open(python_file) as file:
        line = file.readline()
        if key_word in line and "checkMedia" not in line:
            pass


if __name__ == "__main__":
    pass
