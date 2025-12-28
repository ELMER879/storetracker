import sqlite3

DB_NAME = "store.db"


def get_db():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_db() as conn:
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            name TEXT PRIMARY KEY,
            price REAL,
            stock INTEGER
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            approved INTEGER,
            is_admin INTEGER
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL
        )
        """)

        conn.commit()
