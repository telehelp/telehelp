import os

from dotenv import load_dotenv

path = os.getcwd()
load_dotenv(path + "/.env")

from server.api import app  # noqa: E402
