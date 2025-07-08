
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Twitter API Token
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Telegram Chat ID (or target bot ID)
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Polling interval in seconds
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 120))  # default to 30s if not set

# Sanity check to make sure required values are loaded
if not all([TWITTER_BEARER_TOKEN, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    raise ValueError("Missing required environment variables. Check your .env file.")