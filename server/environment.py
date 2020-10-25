import os

BASE_URL = os.getenv("BASE_URL")
ELK_NUMBER = os.getenv("ELK_NUMBER")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
HOOK_URL = os.getenv("HOOK_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

for l in globals():
    print(l)