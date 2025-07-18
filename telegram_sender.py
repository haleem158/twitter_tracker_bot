import requests
import logging
import config
from typing import Optional, Dict, Any
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TelegramError(Exception):
    """Custom exception for Telegram-related errors."""
    pass

def _make_request(method: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Make a request to the Telegram API.
    
    Args:
        method: The Telegram API method to call
        payload: The data to send with the request
    
    Returns:
        Dict containing the response from Telegram
    
    Raises:
        TelegramError: If the request fails or returns an error
    """
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/{method}"
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if not result.get('ok'):
            raise TelegramError(f"Telegram API error: {result.get('description')}")
        
        return result
    except requests.RequestException as e:
        logging.error(f"Failed to send request to Telegram: {str(e)}")
        raise TelegramError(f"Request failed: {str(e)}")
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse Telegram response: {str(e)}")
        raise TelegramError(f"Invalid response from Telegram: {str(e)}")

def send_message(message: str, parse_mode: Optional[str] = None, disable_web_preview: bool = False) -> bool:
    """
    Send a message to the configured Telegram chat.
    
    Args:
        message: The text message to send
        parse_mode: Optional. Can be 'HTML' or 'Markdown'
        disable_web_preview: Optional. Whether to disable web page preview
    
    Returns:
        bool: True if message was sent successfully
    
    Raises:
        TelegramError: If the message couldn't be sent
    """
    try:
        payload = {
            "chat_id": config.TELEGRAM_CHAT_ID,
            "text": message,
            "disable_web_page_preview": disable_web_preview
        }
        
        if parse_mode:
            payload["parse_mode"] = parse_mode
            
        result = _make_request("sendMessage", payload)
        logging.info("Message sent successfully to Telegram")
        return True
        
    except TelegramError as e:
        logging.error(f"Failed to send message: {str(e)}")
        raise

def send_tweet_update(username: str, tweet_url: str) -> bool:
    """
    Send a formatted tweet update message to Telegram.
    
    Args:
        username: The Twitter username
        tweet_url: The URL of the tweet
    
    Returns:
        bool: True if message was sent successfully
    """
    message = (
        f"🔔 New tweet from @{username}\n"
        f"🔗 {tweet_url}"
    )
    return send_message(message, disable_web_preview=False)