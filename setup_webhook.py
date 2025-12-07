import os
import requests

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')  # Your webhook URL (e.g., from Railway, Render, etc.)

def set_webhook():
    """Set Telegram webhook"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    payload = {'url': WEBHOOK_URL}
    
    response = requests.post(url, json=payload)
    print(response.json())

def get_webhook_info():
    """Get current webhook info"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getWebhookInfo"
    response = requests.get(url)
    print(response.json())

if __name__ == '__main__':
    if WEBHOOK_URL:
        print(f"Setting webhook to: {WEBHOOK_URL}")
        set_webhook()
    
    print("\nCurrent webhook info:")
    get_webhook_info()
