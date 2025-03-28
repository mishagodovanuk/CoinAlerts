# services/binance_service.py
import requests
from config import BINANCE_24HR_URL, BINANCE_KLINES_URL, BINANCE_PRICE_URL

class BinanceService:
    """
    Service class to interact with Binance API.
    """
    @staticmethod
    def get_24hr_data(symbol: str) -> dict:
        url = f"{BINANCE_24HR_URL}?symbol={symbol}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_klines(symbol: str, interval: str = "1d", limit: int = 30) -> list:
        url = f"{BINANCE_KLINES_URL}?symbol={symbol}&interval={interval}&limit={limit}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_current_price(symbol: str) -> float:
        url = f"{BINANCE_PRICE_URL}?symbol={symbol}"
        response = requests.get(url)
        response.raise_for_status()
        return float(response.json()["price"])
