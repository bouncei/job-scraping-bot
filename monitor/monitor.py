from telethon import events, functions
from telethon.tl.functions.messages import ImportChatInviteRequest
from monitor.client import client
from bot.functions.keyword import get_keywords


async def join_group(invite_link):
    try:
        await client(ImportChatInviteRequest(invite_link.split('/')[-1]))
        print("Joined the group successfully.")
    except Exception as e:
        print(f"Failed to join group: {e}")

async def monitor_group(group_id):
    keywords = [kw.keyword for kw in get_keywords()]

    @client.on(events.NewMessage(chats=group_id))
    async def handler(event):
        message_text = event.message.message
        if any(keyword.lower() in message_text.lower() for keyword in keywords):
            print(f"Keyword found in message: {message_text}")

    print(f"Monitoring group: {group_id}")

async def get_group_id_from_invite_link(invite_link):
    try:
        result = await client(functions.messages.CheckChatInviteRequest(invite_link.split('/')[-1]))
        if result.chat:
            return result.chat.id
    except Exception as e:
        print(f"Failed to get group ID: {e}")
    return None