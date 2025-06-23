import json
import twitter
import time
import config

# Load usernames from usernames.json
def load_usernames():
    with open("usernames.json", "r") as f:
        data = json.load(f)
    return data["accounts"]

# Load last seen tweet IDs
def load_last_seen():
    try:
        with open("last_seen.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save last seen tweet IDs
def save_last_seen(last_seen):
    with open("last_seen.json", "w") as f:
        json.dump(last_seen, f)

# Main tracking loop
def track_accounts():
    usernames = load_usernames()
    last_seen = load_last_seen()

    for username in usernames:
        tweet_id, tweet_url = twitter.get_latest_tweet(username)
        if tweet_id:
            last_tweet = last_seen.get(username)
            if tweet_id != last_tweet:
                print(f"New tweet from @{username}: {tweet_url}")
                last_seen[username] = tweet_id
            else:
                print(f"No new tweet from @{username}.")
        else:
            print(f"Could not fetch tweet for @{username}.")

    save_last_seen(last_seen)