# main.py
import sys
from services.coingecko_service import CoinGeckoService
from services.price_checker import PriceChecker
from services.telegram_service import TelegramService
from services.subscription_service import SubscriptionService
from config import TELEGRAM_DEFAULT_CHAT_ID

def main():
    # Get list of top 100 coins from CoinGecko.
    try:
        top_coins = CoinGeckoService.get_top_coins()
    except Exception as e:
        print(f"Error fetching top coins: {e}")
        sys.exit(1)

    # Instantiate services
    price_checker = PriceChecker()
    telegram_service = TelegramService()
    subscription_service = SubscriptionService()
    subscribers = subscription_service.get_all_subscribers()

    # If no subscribers, use default for testing (you may change this later)
    if not subscribers:
        subscribers = [TELEGRAM_DEFAULT_CHAT_ID]

    # For each coin, assume the Binance symbol is the coin's symbol in uppercase + "USDT"
    for coin in top_coins:
        # CoinGecko returns "symbol" in lowercase (e.g., "btc")
        symbol = coin["symbol"].upper() + "USDT"
        coin_id = coin["id"]

        result = price_checker.check_coin(symbol, coin_id)
        if result and result.get("alerts"):
            # Compose a message with the alerts
            message = (
                f"🔔 Alert for {result['symbol']}:\n"
                f"Current Price: {result['current_price']} USDT\n"
                + "\n".join(result["alerts"])
            )
            # Send message to all subscribers
            for subscriber in subscribers:
                telegram_service.send_message(subscriber, message)
            print(message)


if __name__ == "__main__":
    main()
