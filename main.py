import config
import twitter
import tracker
import time
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validate_config():
    """Validate that all required configuration variables are set."""
    required_vars = {
        'Twitter Bearer Token': config.TWITTER_BEARER_TOKEN,
        'Telegram Bot Token': config.TELEGRAM_BOT_TOKEN,
        'Telegram Chat ID': config.TELEGRAM_CHAT_ID,
        'Polling Interval': config.POLL_INTERVAL
    }
    
    for name, value in required_vars.items():
        if not value:
            raise ValueError(f"Missing required configuration: {name}")
        logging.info(f"{name} is configured")

def main():
    """Main function to run the Twitter Tracker Bot."""
    try:
        logging.info("Starting Twitter Tracker Bot...")
        validate_config()
        logging.info(f"Polling every {config.POLL_INTERVAL} seconds")

        while True:
            try:
                tracker.track_accounts()
                logging.info("Sleeping until next poll...")
                time.sleep(config.POLL_INTERVAL)
            except Exception as e:
                logging.error(f"Error during tracking: {str(e)}")
                time.sleep(config.POLL_INTERVAL)  # Still sleep before retrying
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()