from pyrogram import Client, filters
from pyrogram.types import *
from info import LOG_CHANNEL

@Client.on_message(filters.command(["bug", "bugs", "feedback"]))
async def bug(client, message):
    if len(message.command) < 2:
        if message.reply_to_message:
            bug = message.reply_to_message.text
        else:
            return await message.reply_text("Please reply to a message or provide error")
    else:
        bug = message.text.split(" ", 1)[1]
    
    await message.reply_text(f"Hi {message.from_user.mention},\nSuccessfully Reported Bugs To My Developer ")
    await client.send_message(LOG_CHANNEL, text=f"#error Bug reported by {message.from_user.mention}: {bug}")
