import sqlite3
from Database.database import get_connection

class User:
    def __init__(self, id: str, name: str, balance: float, is_ai: bool = False, ai_type: str = None):
        self.id = id
        self.name = name
        self.balance = balance
        self.is_ai = is_ai
        self.ai_type = ai_type

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (id, name, balance, is_ai, ai_type) VALUES (?, ?, ?, ?, ?)",
            (self.id, self.name, self.balance, int(self.is_ai), self.ai_type)
        )
        conn.commit()
        conn.close()

    def update(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET name = ?, balance = ?, is_ai = ?, ai_type = ? WHERE id = ?",
            (self.name, self.balance, int(self.is_ai), self.ai_type, self.id)
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
        cursor.execute("SELECT id, name, balance, is_ai, ai_type FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [cls(id=row[0], name=row[1], balance=row[2], is_ai=bool(row[3]), ai_type=row[4]) for row in rows]

    @classmethod
    def find(cls, user_id: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, balance, is_ai, ai_type FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(id=row[0], name=row[1], balance=row[2], is_ai=bool(row[3]), ai_type=row[4]) if row else None
