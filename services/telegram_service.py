# services/telegram_service.py
import requests
import telebot
from config import TELEGRAM_BOT_TOKEN

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

class TelegramService:
    """
    Service class to send messages via Telegram Bot API.
    """
    @staticmethod
    def send_message(chat_id: str, message: str) -> None:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Telegram sending error: {e}")
