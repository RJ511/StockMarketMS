class User:
    def __init__(self, id: int, name: str, balance: float):
        self.id = id
        self.name = name
        self.balance = balance
        self.portfolio = {}  # {stock_ticker: quantity}