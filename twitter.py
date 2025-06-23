import tweepy
import config

# Set up Twitter API client using Tweepy and your bearer token
client = tweepy.Client(bearer_token=config.TWITTER_BEARER_TOKEN)

def get_latest_tweet(username):
    try:
        # Get user info by username
        user = client.get_user(username=username)
        user_id = user.data.id

        # Get the latest tweet from the user's timeline
        tweets = client.get_users_tweets(id=user_id, max_results=5)
        if tweets.data:
            latest_tweet = tweets.data[0]
            tweet_id = latest_tweet.id
            tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"
            return tweet_id, tweet_url
        else:
            return None, None

    except Exception as e:
        print(f"Error fetching tweet for {username}: {e}")
        return None, None