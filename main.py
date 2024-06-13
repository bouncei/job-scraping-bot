import asyncio
import telebot
from config import TELEGRAM_BOT_TOKEN
import bot.commands as commands
import logging
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.




# Initialize Telegram Bot with API token from environment variable
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


# Register bot commands
commands.register_commands(bot)

from monitor.client import start_client


# Run the bot
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_client())
    loop.create_task(bot.polling())
    loop.run_forever()
    print("Bot is polling...")
    # bot.polling()
