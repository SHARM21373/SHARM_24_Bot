import sqlite3
import os

DATABASE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "sharm.db"
)


def get_connection():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            coins INTEGER DEFAULT 0,
            energy INTEGER DEFAULT 1000,
            last_claim TEXT,
            referrals INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
