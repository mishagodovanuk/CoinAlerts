# services/price_checker.py
from utils.file_handler import load_json, save_json
from config import COIN_STATE_FILE
from services.binance_service import BinanceService
from services.coingecko_service import CoinGeckoService

class PriceChecker:
    """
    Checks if a coin's price has broken through defined thresholds.
    It compares current price against daily, monthly, and all-time thresholds.
    It also uses stored previous state to only notify on transitions.
    """

    def __init__(self):
        self.state = load_json(COIN_STATE_FILE)

    def _update_state(self, symbol: str, coin_state: dict) -> None:
        self.state[symbol] = coin_state
        save_json(COIN_STATE_FILE, self.state)

    def check_coin(self, symbol: str, coin_id: str) -> dict:
        """
        Fetches data for the given coin and returns any threshold breaches.
        Also updates the internal state.
        Returns a dictionary with alert messages if any thresholds are broken.
        """
        alerts = []
        coin_state = self.state.get(symbol, {})

        # Get Binance data
        try:
            data_24hr = BinanceService.get_24hr_data(symbol)
            daily_low = float(data_24hr["lowPrice"])
            daily_high = float(data_24hr["highPrice"])

            klines = BinanceService.get_klines(symbol, limit=30)
            monthly_low = min(float(kline[3]) for kline in klines)
            monthly_high = max(float(kline[2]) for kline in klines)

            current_price = BinanceService.get_current_price(symbol)
        except Exception as e:
            print(f"Error fetching Binance data for {symbol}: {e}")
            return {}

        # Get CoinGecko data (all-time thresholds)
        try:
            all_time_data = CoinGeckoService.get_all_time_data(coin_id)
            all_time_high = all_time_data["all_time_high"]
            all_time_low = all_time_data["all_time_low"]
        except Exception as e:
            print(f"Error fetching CoinGecko data for {coin_id}: {e}")
            return {}

        # Initialize previous state if missing
        if "last_price" not in coin_state:
            coin_state["last_price"] = current_price
            # Threshold flags help to avoid duplicate alerts
            coin_state["daily_high_triggered"] = False
            coin_state["daily_low_triggered"] = False
            coin_state["monthly_high_triggered"] = False
            coin_state["monthly_low_triggered"] = False
            coin_state["all_time_high_triggered"] = False
            coin_state["all_time_low_triggered"] = False

        last_price = coin_state["last_price"]

        # Check daily thresholds
        if current_price > daily_high and last_price <= daily_high and not coin_state["daily_high_triggered"]:
            alerts.append(f"Exceeded Daily High: {daily_high} USDT")
            coin_state["daily_high_triggered"] = True
        elif current_price <= daily_high:
            coin_state["daily_high_triggered"] = False

        if current_price < daily_low and last_price >= daily_low and not coin_state["daily_low_triggered"]:
            alerts.append(f"Dropped below Daily Low: {daily_low} USDT")
            coin_state["daily_low_triggered"] = True
        elif current_price >= daily_low:
            coin_state["daily_low_triggered"] = False

        # Check monthly thresholds
        if current_price > monthly_high and last_price <= monthly_high and not coin_state["monthly_high_triggered"]:
            alerts.append(f"Exceeded Monthly High: {monthly_high} USDT")
            coin_state["monthly_high_triggered"] = True
        elif current_price <= monthly_high:
            coin_state["monthly_high_triggered"] = False

        if current_price < monthly_low and last_price >= monthly_low and not coin_state["monthly_low_triggered"]:
            alerts.append(f"Dropped below Monthly Low: {monthly_low} USDT")
            coin_state["monthly_low_triggered"] = True
        elif current_price >= monthly_low:
            coin_state["monthly_low_triggered"] = False

        # Check all-time thresholds
        if current_price > all_time_high and last_price <= all_time_high and not coin_state["all_time_high_triggered"]:
            alerts.append(f"Exceeded All-Time High: {all_time_high} USDT")
            coin_state["all_time_high_triggered"] = True
        elif current_price <= all_time_high:
            coin_state["all_time_high_triggered"] = False

        if current_price < all_time_low and last_price >= all_time_low and not coin_state["all_time_low_triggered"]:
            alerts.append(f"Dropped below All-Time Low: {all_time_low} USDT")
            coin_state["all_time_low_triggered"] = True
        elif current_price >= all_time_low:
            coin_state["all_time_low_triggered"] = False

        coin_state["last_price"] = current_price
        self._update_state(symbol, coin_state)

        return {
            "symbol": symbol,
            "current_price": current_price,
            "alerts": alerts
        }
