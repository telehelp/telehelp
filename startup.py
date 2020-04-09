import os

from dotenv import load_dotenv

from server.api import app

path = os.getcwd()
load_dotenv(path + "/.env")
