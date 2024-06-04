# main.py

import telebot
from dotenv import load_dotenv
import os
import bot.commands as commands

# Load environment variables from .env file
load_dotenv()

# Initialize Telegram Bot with API token from environment variable
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

# Define the database URL
db_url = os.getenv("DB_URL")

# Register bot commands
commands.register_commands(bot)

# Run the bot
if __name__ == "__main__":
    print("Bot running...")
    bot.polling()
