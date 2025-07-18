import json
import twitter
import time
import config
import logging
import os
from typing import Dict, List, Optional
from telegram_sender import send_tweet_update, TelegramError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TrackerError(Exception):
    """Custom exception for tracking-related errors."""
    pass

def load_usernames() -> List[str]:
    """
    Load Twitter usernames from usernames.json file.
    
    Returns:
        List[str]: List of Twitter usernames to track
    
    Raises:
        TrackerError: If the file cannot be read or parsed
    """
    try:
        with open("usernames.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data.get("accounts"), list):
                raise TrackerError("Invalid usernames.json format: 'accounts' must be a list")
            return data["accounts"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        raise TrackerError(f"Failed to load usernames: {str(e)}")

def load_last_seen() -> Dict[str, str]:
    """
    Load last seen tweet IDs from last_seen.json file.
    
    Returns:
        Dict[str, str]: Dictionary mapping usernames to their last seen tweet IDs
    """
    try:
        if not os.path.exists("last_seen.json"):
            logging.info("No last_seen.json found, starting fresh")
            return {}
            
        with open("last_seen.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                logging.warning("Invalid last_seen.json format, starting fresh")
                return {}
            return data
    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Error loading last_seen.json: {str(e)}, starting fresh")
        return {}

def save_last_seen(last_seen: Dict[str, str]) -> None:
    """
    Save last seen tweet IDs to last_seen.json file.
    
    Args:
        last_seen: Dictionary mapping usernames to their last seen tweet IDs
    
    Raises:
        TrackerError: If the file cannot be written
    """
    try:
        with open("last_seen.json", "w", encoding='utf-8') as f:
            json.dump(last_seen, f, indent=2)
    except (IOError, OSError) as e:
        raise TrackerError(f"Failed to save last seen tweets: {str(e)}")

def process_new_tweet(username: str, tweet_id: str, tweet_url: str) -> None:
    """
    Process a new tweet by sending it to Telegram.
    
    Args:
        username: The Twitter username
        tweet_id: The ID of the tweet
        tweet_url: The URL of the tweet
    """
    try:
        logging.info(f"New tweet found from @{username}")
        send_tweet_update(username, tweet_url)
    except TelegramError as e:
        logging.error(f"Failed to send tweet update for @{username}: {str(e)}")

def track_accounts() -> None:
    """
    Main tracking function that checks for new tweets from all tracked accounts.
    """
    try:
        usernames = load_usernames()
        last_seen = load_last_seen()
        updates_found = False

        for username in usernames:
            try:
                logging.debug(f"Checking tweets for @{username}")
                tweet_id, tweet_url = twitter.get_latest_tweet(username)
                
                if tweet_id:
                    last_tweet = last_seen.get(username)
                    if tweet_id != last_tweet:
                        process_new_tweet(username, tweet_id, tweet_url)
                        last_seen[username] = tweet_id
                        updates_found = True
                    else:
                        logging.debug(f"No new tweets from @{username}")
                else:
                    logging.warning(f"Could not fetch tweets for @{username}")
                    
            except Exception as e:
                logging.error(f"Error processing @{username}: {str(e)}")
                continue  # Continue with next user even if one fails
                
        if updates_found:
            save_last_seen(last_seen)
            
    except TrackerError as e:
        logging.error(f"Tracking error: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in track_accounts: {str(e)}")
        raise