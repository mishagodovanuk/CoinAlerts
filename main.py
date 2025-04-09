import sys
import time
import threading
from services.coingecko_service import CoinGeckoService
from services.price_checker import PriceChecker
from services.telegram_service import TelegramService, bot
from services.subscription_service import SubscriptionService
from config import TELEGRAM_DEFAULT_CHAT_ID
from telebot import types


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = str(message.chat.id)
    subscription_service = SubscriptionService()

    # Create persistent reply keyboard
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Subscribe ✅"))

    if chat_id not in subscription_service.get_all_subscribers():
        bot.send_message(chat_id, "Welcome! Click the button below to subscribe to alerts.", reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "You're already subscribed to alerts. Stay tuned 🚀", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Subscribe ✅")
def handle_subscribe_btn(message):
    chat_id = str(message.chat.id)
    subscription_service = SubscriptionService()

    if chat_id in subscription_service.get_all_subscribers():
        bot.send_message(chat_id, "You're already subscribed ✅")
    else:
        subscription_service.add_subscriber(chat_id)
        bot.send_message(chat_id, "🎉 You have been subscribed to alerts!")


# Background price check logic
def run_price_checker():
    while True:
        try:
            top_coins = CoinGeckoService.get_top_coins()
        except Exception as e:
            print(f"Error fetching top coins: {e}")
            time.sleep(60)
            continue

        price_checker = PriceChecker()
        telegram_service = TelegramService()
        subscription_service = SubscriptionService()
        subscribers = subscription_service.get_all_subscribers()

        if not subscribers:
            subscribers = [TELEGRAM_DEFAULT_CHAT_ID]

        for coin in top_coins:
            symbol = coin["symbol"].upper() + "USDT"
            coin_id = coin["id"]

            result = price_checker.check_coin(symbol, coin_id)
            if result and result.get("alerts"):
                message = (
                    f"\U0001F514 Alert for {result['symbol']}:\n"
                    f"Current Price: {result['current_price']} USDT\n"
                    + "\n".join(result["alerts"])
                )
                for subscriber in subscribers:
                    telegram_service.send_message(subscriber, message)
                print(message)

        time.sleep(300)  # Wait 5 minutes before next check

if __name__ == "__main__":
    # Start price checker in background
    checker_thread = threading.Thread(target=run_price_checker, daemon=True)
    checker_thread.start()

    # Start Telegram bot
    bot.infinity_polling()
