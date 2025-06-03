class Transaction:
    def __init__(self, buyer_id: int, seller_id: int, stock_ticker: str, quantity: int, price: float):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.stock_ticker = stock_ticker
        self.quantity = quantity
        self.price = price
        self.timestamp = None
