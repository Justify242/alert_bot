import os

from dotenv import load_dotenv

load_dotenv(override=True)

DB_NAME = "database.db"

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
BOT_ADMINS = str(os.getenv("BOT_ADMINS", "")).split(";")

OPEN_WEATHER_MAP_KEY = str(os.getenv("OPEN_WEATHER_MAP_KEY"))