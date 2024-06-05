# main.py

import telebot
from dotenv import load_dotenv
import os
import bot.commands as commands

# Load environment variables from .env file
load_dotenv()

# Initialize Telegram Bot with API token from environment variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if TELEGRAM_BOT_TOKEN is None:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")


# Initialize Telegram Bot with API token from environment variable
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)



# Register bot commands
commands.register_commands(bot)

# Run the bot
if __name__ == "__main__":
    print("Bot is polling...")
    bot.polling(none_stop=True)
