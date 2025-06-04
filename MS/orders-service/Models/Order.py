# Models/Order.py
import sqlite3
from Database.database import get_connection

class Order:
    def __init__(self, id: str, user_id: str, stock_id: str, type: str, quantity: int, price: float):
        self.id = id
        self.user_id = user_id
        self.stock_id = stock_id
        self.type = type  # "buy" ou "sell"
        self.quantity = quantity
        self.price = price

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (id, user_id, stock_id, type, quantity, price) VALUES (?, ?, ?, ?, ?, ?)",
            (self.id, self.user_id, self.stock_id, self.type, self.quantity, self.price)
        )
        conn.commit()
        conn.close()

    def update(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE orders SET user_id = ?, stock_id = ?, type = ?, quantity = ?, price = ? WHERE id = ?",
            (self.user_id, self.stock_id, self.type, self.quantity, self.price, self.id)
        )
        conn.commit()
        conn.close()

    def delete(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, stock_id, type, quantity, price FROM orders")
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def find(cls, order_id: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, stock_id, type, quantity, price FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None
