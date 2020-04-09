import os
from dotenv import load_dotenv

path = os.getcwd()
print(path)
load_dotenv(path+'/.env')

from server.api import app
