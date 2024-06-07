from telethon import events
from monitor.client import client
from bot.models.keyword import get_all_keywords

async def join_group(invite_link):
    try:
        await client(ImportChatInviteRequest(invite_link.split('/')[-1]))
        print("Joined the group successfully.")
    except Exception as e:
        print(f"Failed to join group: {e}")

async def monitor_group(group_id):
    keywords = [kw.keyword for kw in get_all_keywords()]

    @client.on(events.NewMessage(chats=group_id))
    async def handler(event):
        message_text = event.message.message
        if any(keyword.lower() in message_text.lower() for keyword in keywords):
            print(f"Keyword found in message: {message_text}")

    print(f"Monitoring group: {group_id}")

async def get_group_id_from_invite_link(invite_link):
    # Implement this function to get the group ID from the invite link
    return group_id
