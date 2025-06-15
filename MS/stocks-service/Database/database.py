import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "stocks.db")  # aponta para Database/stocks.db

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_stock_price_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT stock_id FROM stock_prices")
    stock_ids = [row[0] for row in cursor.fetchall()]

    data = {}
    for stock_id in stock_ids:
        cursor.execute("""
            SELECT date, price FROM stock_prices
            WHERE stock_id = ?
            ORDER BY date ASC
        """, (stock_id,))
        rows = cursor.fetchall()
        data[stock_id] = {
            "labels": [r[0][:10] for r in rows],
            "prices": [r[1] for r in rows]
        }

    conn.close()
    return data

def save_price_history(stock_id: str, price: float):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO stock_prices (stock_id, date, price)
        VALUES (?, ?, ?)
    """, (stock_id, datetime.now().isoformat(), price))
    conn.commit()
    conn.close()