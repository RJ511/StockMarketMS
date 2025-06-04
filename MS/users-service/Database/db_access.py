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

def get_user_by_id(user_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, balance FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return User(id=row[0], name=row[1], balance=row[2]) if row else None

def update_user_by_id(user_id: str, name: str, balance: float):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, balance = ? WHERE id = ?", (name, balance, user_id))
    conn.commit()
    conn.close()

def update_user_balance_by_id(user_id: str, balance: float):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (balance, user_id))
    conn.commit()
    conn.close()

def delete_user_by_id(user_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

