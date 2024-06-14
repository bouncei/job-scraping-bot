from telethon import TelegramClient, events
from config import API_ID, API_HASH, USER_ID
from bot.functions import channel, keyword

channels = channel.get_channels(USER_ID)
keywords = keyword.get_keywords(USER_ID)

KEYWORDS_TEXT = [keyword.keyword for keyword in keywords]
CHANNEL_IDS = [channel.channel_id for channel in channels]

client = TelegramClient('monitor', API_ID, API_HASH)



async def start_client():
    await client.start()


@client.on(events.NewMessage(chats=CHANNEL_IDS))
async def handler(event):
    message_text = event.message.message
    if any(keyword in message_text for keyword in KEYWORDS_TEXT):
        await client.send_message(USER_ID, f"Keyword found: {message_text}")
