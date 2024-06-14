from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if TELEGRAM_BOT_TOKEN is None:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")


API_ID = os.getenv("API_ID")
if API_ID is None:
    raise ValueError("No API_ID found in environment variables")

API_HASH = os.getenv("API_HASH")
if API_HASH is None:
    raise ValueError("No API_HASH found in environment variables")

USER_ID = os.getenv("USER_ID")
if USER_ID is None:
    raise ValueError("No USER_ID found in environment variables")
