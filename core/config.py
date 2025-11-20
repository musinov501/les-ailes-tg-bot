import os

from dotenv import load_dotenv

load_dotenv(
    dotenv_path = ".env"
)


BOT_TOKEN = os.getenv("BOT_TOKEN")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DB_CONIFG = {
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT
}


DEVELOPER = int(os.getenv("DEVELOPER"))






