import requests
import os
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")


def send_announcement_to_telegram(announcement):
    text = f"📢 <b>{announcement.title}</b>\n\n{announcement.message}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegramga yuborishda xatolik: {e}")
