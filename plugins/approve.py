import logging
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserIsBlocked, PeerIdInvalid
from pyrogram.enums import ParseMode
import datetime

# Configure logging for better error tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration options (can be extended as needed)
CONFIG = {
    "bot_username": "mmwbotz_bot",
    "main_channel_url": "https://t.me/MRXSUPPORTS",
    "ott_updates_channel_url": "https://t.me/MRXSUPPORTS",
    "photo_url": "https://envs.sh/zay.jpg",  # Replace with your actual image URL
    "welcome_message": "**{greeting} {name} 👻\n\nWelcome to {chat_name}! Your request has been approved.\n\nSend /start to know more.**",
    "greeting_messages": {
        'en': ['Good Morning', 'Good Afternoon', 'Good Evening'],
        'ru': ['Доброе утро', 'Добрый день', 'Добрый вечер']
    }
}

def get_greeting(language: str):
    """Return a greeting message based on the time of day."""
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        greeting_index = 0  # Good Morning
    elif 12 <= current_hour < 18:
        greeting_index = 1  # Good Afternoon
    else:
        greeting_index = 2  # Good Evening
    
    # Fallback to English if the user's language is not in the config
    return CONFIG["greeting_messages"].get(language, CONFIG["greeting_messages"]['en'])[greeting_index]

@Client.on_chat_join_request()
async def accept_request(client, r):
    """Handles chat join requests, sends a welcome message, and approves the request."""
    
    try:
        # Create Inline Keyboard
        rm = InlineKeyboardMarkup([
            [InlineKeyboardButton('🎉 Add Me To Your Groups 🎉', url=f'http://t.me/{CONFIG["bot_username"]}?startgroup=true')],
            [
                InlineKeyboardButton('OTT Updates', url=CONFIG["ott_updates_channel_url"]),
                InlineKeyboardButton('Main Channel', url=CONFIG["main_channel_url"]),
            ]
        ])

        # Determine greeting based on the user's language (default to 'en' if unavailable)
        greeting = get_greeting(r.from_user.language_code or 'en')

        # Prepare the personalized welcome message
        welcome_text = CONFIG["welcome_message"].format(
            greeting=greeting, 
            name=r.from_user.first_name or r.from_user.username,  # Fallback to username if no first name
            chat_name=r.chat.title
        )
        
        # Ensure the photo URL is valid (you may want to add checks or use a default image if invalid)
        photo_url = CONFIG["photo_url"]

        # Attempt to send the photo with the welcome message
        await client.send_photo(
            r.from_user.id,
            photo_url,
            welcome_text,
            reply_markup=rm,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Approve the request after the message has been successfully sent
        await r.approve()

        logger.info(f"Successfully processed join request from {r.from_user.username} in {r.chat.title}")
    
    except UserIsBlocked:
        logger.warning(f"User {r.from_user.username} has blocked the bot.")
    except PeerIdInvalid:
        logger.error(f"Invalid Peer ID when processing request for {r.from_user.username}.")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

