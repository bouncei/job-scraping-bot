from telethon import TelegramClient
from config import API_ID, API_HASH


client = TelegramClient('session_name', API_ID, API_HASH)

async def start_client():
    await client.start()
