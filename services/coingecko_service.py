# services/coingecko_service.py
import requests
from config import COINGECKO_TOP_COINS_URL, COINGECKO_COIN_URL
from pprint import pprint

class CoinGeckoService:
    """
    Service class to interact with the CoinGecko API.
    """
    @staticmethod
    def get_top_coins(vs_currency: str = "usd", per_page: int = 100, page: int = 1) -> list:
        params = {
            "vs_currency": vs_currency,
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page,
            "sparkline": False
        }
        response = requests.get(COINGECKO_TOP_COINS_URL, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_all_time_data(coin_id: str) -> dict:
        url = f"{COINGECKO_COIN_URL}/{coin_id}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pprint(data)
        return {
            "all_time_high": data["market_data"]["ath"]["usd"],
            "all_time_low": data["market_data"]["atl"]["usd"]
        }
