import sqlite3
import os
from datetime import datetime

# Define o caminho da base de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "stocks.db")

# Cria a ligação
def get_connection():
    return sqlite3.connect(DB_PATH)

# Inicializa todas as tabelas
def init_db():
    create_stock_table()
    create_stock_history_table()
    print("✔️ Base de dados inicializada com sucesso.")

def create_stock_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def create_stock_history_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id TEXT NOT NULL,
            date TEXT NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(stock_id) REFERENCES stocks(id)
        )
    """)
    conn.commit()
    conn.close()
    print("✔️ Tabela de histórico de preços criada com sucesso.")

# Guarda histórico de preço
def save_price_history(stock_id: str, price: float):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO stock_prices (stock_id, date, price)
        VALUES (?, ?, ?)
    """, (stock_id, datetime.now().isoformat(), price))
    conn.commit()
    conn.close()

# Exporta histórico como JSON
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

# Só corre se executar diretamente este ficheiro
if __name__ == "__main__":
    init_db()
