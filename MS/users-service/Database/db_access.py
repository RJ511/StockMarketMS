from .database import get_connection
from Models.User import User

def insert_user(id: str, name: str, balance: float = 0.0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (id, name, balance) VALUES (?, ?, ?)",
        (id, name, balance)
    )
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, balance FROM users")
    rows = cursor.fetchall()
    conn.close()
    return [User(id=row[0], name=row[1], balance=row[2]) for row in rows]
