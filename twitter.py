import tweepy
import config
import logging
import time
from typing import Optional, Tuple, Dict, Any
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TwitterError(Exception):
    """Custom exception for Twitter-related errors."""
    pass

class RateLimitError(TwitterError):
    """Raised when Twitter API rate limits are hit."""
    pass

class TwitterClient:
    def __init__(self):
        """Initialize the Twitter API client with rate limiting protection."""
        if not config.TWITTER_BEARER_TOKEN:
            raise TwitterError("Twitter Bearer Token is not configured")
            
        self.client = tweepy.Client(
            bearer_token=config.TWITTER_BEARER_TOKEN,
            wait_on_rate_limit=True  # Auto-wait when rate limited
        )
        self.user_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_duration = timedelta(hours=1)  # Cache user IDs for 1 hour

    def _get_user_id(self, username: str) -> str:
        """
        Get user ID from username with caching.
        
        Args:
            username: Twitter username without @ symbol
        
        Returns:
            str: Twitter user ID
            
        Raises:
            TwitterError: If user cannot be found or API error occurs
        """
        # Check cache first
        if username in self.user_cache:
            cache_data = self.user_cache[username]
            if datetime.now() - cache_data['timestamp'] < self.cache_duration:
                logging.debug(f"Using cached user ID for @{username}")
                return cache_data['user_id']
        
        try:
            logging.debug(f"Fetching user ID for @{username}")
            user = self.client.get_user(username=username)
            
            if not user.data:
                raise TwitterError(f"User @{username} not found")
                
            # Update cache
            self.user_cache[username] = {
                'user_id': user.data.id,
                'timestamp': datetime.now()
            }
            
            return user.data.id
            
        except tweepy.TooManyRequests:
            raise RateLimitError(f"Rate limit reached while fetching user @{username}")
        except tweepy.HTTPException as e:
            raise TwitterError(f"Twitter API error for @{username}: {str(e)}")

    def get_latest_tweet(self, username: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Get the latest tweet from a user.
        
        Args:
            username: Twitter username without @ symbol
            
        Returns:
            Tuple containing (tweet_id, tweet_url) if found, (None, None) if no tweets
            
        Raises:
            TwitterError: If API error occurs
            RateLimitError: If rate limit is hit
        """
        try:
            user_id = self._get_user_id(username)
            
            # Get recent tweets, excluding replies and retweets
            tweets = self.client.get_users_tweets(
                id=user_id,
                max_results=5,
                exclude=['retweets', 'replies']
            )
            
            if not tweets.data:
                logging.info(f"No tweets found for @{username}")
                return None, None
                
            latest_tweet = tweets.data[0]
            tweet_id = str(latest_tweet.id)  # Convert to string for consistency
            tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"
            
            logging.debug(f"Found tweet from @{username}: {tweet_url}")
            return tweet_id, tweet_url
            
        except RateLimitError:
            logging.warning(f"Rate limit reached for @{username}, will retry later")
            raise
        except TwitterError as e:
            logging.error(f"Error fetching tweets for @{username}: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error for @{username}: {str(e)}")
            raise TwitterError(f"Unexpected error: {str(e)}")

# Initialize global client instance
twitter = TwitterClient()