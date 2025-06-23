import requests
import config

def send_message(message):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
    else:
        print("Message sent to Telegram successfully.")