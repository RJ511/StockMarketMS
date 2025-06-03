class Order:
    def __init__(self, id: int, user_id: int, stock_ticker: str, order_type: str, quantity: int, limit_price: float):
        self.id = id
        self.user_id = user_id
        self.stock_ticker = stock_ticker
        self.order_type = order_type  # 'buy' or 'sell'
        self.quantity = quantity
        self.limit_price = limit_price
        self.status = "pending"