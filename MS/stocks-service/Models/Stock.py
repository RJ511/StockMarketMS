import sqlite3
from Database.database import get_connection

class Stock:
    def __init__(self, id: str, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO stocks (id, name, price) VALUES (?, ?, ?)",
            (self.id, self.name, self.price)
        )
        conn.commit()
        conn.close()

    def update(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE stocks SET name = ?, price = ? WHERE id = ?",
            (self.name, self.price, self.id)
        )
        conn.commit()
        conn.close()

    def delete(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stocks WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM stocks")
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=r[0], name=r[1], price=r[2]) for r in rows]

    @classmethod
    def find(cls, stock_id: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM stocks WHERE id = ?", (stock_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(id=row[0], name=row[1], price=row[2]) if row else None
    
    def update_stock_price(stock_id: str, new_price: float):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE stocks SET price = ? WHERE id = ?",
            (new_price, stock_id)
        )
        conn.commit()
        conn.close()

