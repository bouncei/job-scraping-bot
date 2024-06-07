import asyncio
import telebot
from dotenv import load_dotenv
import os
import bot.commands as commands
import logging
from monitor.client import start_client
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

# Load environment variables from .env file
load_dotenv()

# Initialize Telegram Bot with API token from environment variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if TELEGRAM_BOT_TOKEN is None:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")


API_ID = os.getenv("API_ID")
if API_ID is None:
    raise ValueError("No API_ID found in environment variables")

API_HASH = os.getenv("API_HASH")
if API_HASH is None:
    raise ValueError("No API_HASH found in environment variables")


# Initialize Telegram Bot with API token from environment variable
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


# Register bot commands
commands.register_commands(bot)

# Run the bot
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_client())
    loop.create_task(bot.polling())
    loop.run_forever()
    print("Bot is polling...")
    # bot.polling()
