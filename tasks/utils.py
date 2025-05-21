import requests
from django.conf import settings


def send_telegram_message(chat_id, message):
    if not chat_id:
        return
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "message": message})