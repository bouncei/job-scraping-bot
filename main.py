# main.py

import telebot
from dotenv import load_dotenv
import os
import bot.commands as commands

# Load environment variables from .env file
load_dotenv()

# Initialize Telegram Bot with API token from environment variable
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

# Register bot commands
commands.register_commands(bot)

# Run the bot
if __name__ == "__main__":
    print("Bot running...")
    bot.polling()
