# config.py

# Telegram configuration
TELEGRAM_BOT_TOKEN = '7373123208:AAEo8WP3XykO7neTVM_RYKJjVQRrnD4N5Ec'
# This chat id may be a group or personal chat. When sending alerts, they will be broadcast
# to all subscribers from subscribers.json.
TELEGRAM_DEFAULT_CHAT_ID = 'your_default_chat_id'

# File paths for persistence
SUBSCRIBERS_FILE = 'data/subscribers.json'
COIN_STATE_FILE = 'data/coin_state.json'

# Binance API URLs
BINANCE_24HR_URL = "https://api.binance.com/api/v3/ticker/24hr"
BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"
BINANCE_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"

# CoinGecko API URL
COINGECKO_TOP_COINS_URL = "https://api.coingecko.com/api/v3/coins/markets"
COINGECKO_COIN_URL = "https://api.coingecko.com/api/v3/coins"
