import sqlite3

DB_NAME = "store.db"


def get_db():
    """Connect to SQLite database"""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Create tables if they don't exist"""
    with get_db() as conn:
        cur = conn.cursor()

        # Products table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            name TEXT PRIMARY KEY,
            price REAL,
            stock INTEGER
        )
        """)

        # Users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            approved INTEGER,
            is_admin INTEGER
        )
        """)

        # Sales table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL
        )
        """)

        conn.commit()
