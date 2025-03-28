# models/coin.py

class Coin:
    """
    Represents a coin with its trading symbol and CoinGecko id.
    """
    def __init__(self, symbol: str, coin_id: str):
        self.symbol = symbol  # For Binance e.g. "BTCUSDT"
        self.coin_id = coin_id  # For CoinGecko e.g. "bitcoin"
