import config
import twitter
import tracker
import time

def main():
    print("Starting Twitter Tracker Bot...")
    print("Polling every", config.POLL_INTERVAL, "seconds")

    while True:
        tracker.track_accounts()
        print("Sleeping...\n")
        time.sleep(config.POLL_INTERVAL)

if __name__ == "__main__":
    main()
"""def main():
    print("Twitter Bearer Token:", config.TWITTER_BEARER_TOKEN)
    print("Telegram Bot Token:", config.TELEGRAM_BOT_TOKEN)
    print("Telegram Chat ID:", config.TELEGRAM_CHAT_ID)
    print("Polling Interval:", config.POLL_INTERVAL)

    # Replace 'jack' with any public Twitter handle you want to test
    username = "haleemisthename"
    tweet_id, tweet_url = twitter.get_latest_tweet(username)
    if tweet_id:
        print(f"Latest tweet from @{username}: {tweet_url}")
    else:
        print(f"No tweets found for @{username}")

if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()"""