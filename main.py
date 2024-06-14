import asyncio
import telebot
from telethon import TelegramClient, events
from config import TELEGRAM_BOT_TOKEN, API_ID, API_HASH, USER_ID
import bot.commands as commands
from bot.functions import channel, keyword
import logging
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize Telegram Bot with API token from environment variable
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


# Register bot commands
commands.register_commands(bot)


channels = channel.get_channels(USER_ID)
keywords = keyword.get_keywords(USER_ID)

KEYWORDS_TEXT = [keyword.keyword for keyword in keywords]
CHANNEL_IDS = [channel.channel_id for channel in channels]


# Initialize Telethon client
client = TelegramClient('monitor_bot', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNEL_IDS))
async def handler(event):
    message_text = event.message.message
    if any(keyword in message_text for keyword in KEYWORDS_TEXT):
        try:
            await bot.send_message(USER_ID, f"Keyword found: {message_text}")
            logger.info(f"Keyword found in message: {message_text}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")


async def main():
    logger.info("Starting bot and monitoring channels...")

    # Start Telethon client
    await client.start()

    # Run Telethon client until disconnected
    telethon_task = asyncio.create_task(client.run_until_disconnected())

    # Run Telebot in a separate thread to keep it non-blocking
    loop = asyncio.get_event_loop()
    telebot_task = loop.run_in_executor(None, bot.polling)

    # Wait for both tasks to complete
    await asyncio.gather(telethon_task, telebot_task)

if __name__ == "__main__":
    logger.info("Keyyy words: %s", KEYWORDS_TEXT)
    asyncio.run(main())
