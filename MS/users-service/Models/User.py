import sqlite3
from Database.database import get_connection

class User:
    def __init__(self, id: str, name: str, balance: float):
        self.id = id
        self.name = name
        self.balance = balance

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (id, name, balance) VALUES (?, ?, ?)",
            (self.id, self.name, self.balance)
        )
        conn.commit()
        conn.close()

    def update(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET name = ?, balance = ? WHERE id = ?",
            (self.name, self.balance, self.id)
        )
        conn.commit()
        conn.close()

    def delete(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, balance FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], name=row[1], balance=row[2]) for row in rows]

    @classmethod
    def find(cls, user_id: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, balance FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(id=row[0], name=row[1], balance=row[2]) if row else None
