# Models/Transaction.py
import sqlite3
from Database.database import get_connection

class Transaction:
    def __init__(self, id: str, buyer_id: str, seller_id: str, stock_id: str, quantity: int, price: float):
        self.id = id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.stock_id = stock_id
        self.quantity = quantity
        self.price = price

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO transactions (id, buyer_id, seller_id, stock_id, quantity, price)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (self.id, self.buyer_id, self.seller_id, self.stock_id, self.quantity, self.price)
        )
        conn.commit()
        conn.close()

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, buyer_id, seller_id, stock_id, quantity, price FROM transactions")
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]
