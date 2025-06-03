class Stock:
    def __init__(self, ticker: str, name: str, price: float):
        self.ticker = ticker
        self.name = name
        self.price = price
        self.price_history = []  # list of (timestamp, price)