from database import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL DEFAULT 10000
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✔️ Base de dados criada ou atualizada com sucesso.")
