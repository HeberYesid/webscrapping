import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram_alert(message):
    """
    Sends a message to the configured Telegram chat.
    """
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: Telegram credentials not found in .env")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Alert sent: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram alert: {e}")
