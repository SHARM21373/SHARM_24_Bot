import os
import sqlite3

# =====================================
# Application
# =====================================

APP_NAME = "SHARM Mining"
APP_VERSION = "1.0.0"


# =====================================
# Telegram
# =====================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "")


# =====================================
# Database
# =====================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

DATABASE_PATH = os.path.join(DATA_DIR, "sharm.db")


def get_connection():
    os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# =====================================
# Mining
# =====================================

DEFAULT_BALANCE = 0

DEFAULT_BATTERY = 1500

MAX_BATTERY = 1500

POINT_PER_TAP = 1

PROCESSING_SECONDS = 3

BATTERY_RECHARGE_SECONDS = 60


# =====================================
# Referral
# =====================================

REFERRAL_REWARD = 100


# =====================================
# Security
# =====================================

REQUEST_LIMIT_PER_SECOND = 5


# =====================================
# UI
# =====================================

APP_THEME = "dark"

COIN_NAME = "SHARM"


# =====================================
# Future Features
# =====================================

ENABLE_AIRDROP = False

ENABLE_TOKEN = False

ENABLE_WITHDRAW = False

ENABLE_UPGRADE = False


# =====================================
# Database Initialization
# =====================================

def init_db():

    os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()


    # ======================================
    # USERS
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        telegram_id INTEGER PRIMARY KEY,

        username TEXT DEFAULT '',

        first_name TEXT DEFAULT '',

        balance INTEGER DEFAULT 0,

        battery INTEGER DEFAULT 1500,

        max_battery INTEGER DEFAULT 1500,

        tap_power INTEGER DEFAULT 1,

        mine_level INTEGER DEFAULT 1,

        referrals INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    # ======================================
    # USERS DATABASE MIGRATION
    # ======================================

    cursor.execute("PRAGMA table_info(users)")

    existing_columns = {
        row[1]
        for row in cursor.fetchall()
    }


    # Add missing username column
    if "username" not in existing_columns:

        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN username TEXT DEFAULT ''
        """)


    # Add missing first_name column
    if "first_name" not in existing_columns:

        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN first_name TEXT DEFAULT ''
        """)


    # Add missing balance column
    if "balance" not in existing_columns:

        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN balance INTEGER DEFAULT 0
        """)


    # Add missing battery column
    if "battery" not in existing_columns:

        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN battery INTEGER DEFAULT 1500
        """)


    # Add missing max_battery column
    if "max_battery" not in existing_columns:

        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN max_battery INTEGER DEFAULT 1500
        """)


    # Add missing tap_power column
    if "tap_power" not in existing_columns:

        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN tap_power INTEGER DEFAULT 1
        """)


    # Add missing mine_level column
    if "mine_level" not in existing_columns:

        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN mine_level INTEGER DEFAULT 1
        """)


    # Add missing referrals column
    if "referrals" not in existing_columns:

        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN referrals INTEGER DEFAULT 0
        """)


    # Add missing created_at column
    if "created_at" not in existing_columns:

        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN created_at TIMESTAMP
        """)


    # Add missing updated_at column
    if "updated_at" not in existing_columns:

        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN updated_at TIMESTAMP
        """)


    # Add missing last_login column
    if "last_login" not in existing_columns:

        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN last_login TIMESTAMP
        """)


    # ======================================
    # SHOP UPGRADES
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shop_upgrades (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        description TEXT,

        price INTEGER NOT NULL,

        effect_type TEXT,

        effect_value INTEGER,

        max_level INTEGER DEFAULT 10,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    # ======================================
    # USER UPGRADES
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_upgrades (

        telegram_id INTEGER NOT NULL,

        upgrade_name TEXT NOT NULL,

        level INTEGER DEFAULT 1,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        PRIMARY KEY (telegram_id, upgrade_name)

    )
    """)


    # ======================================
    # ANNOUNCEMENTS
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS announcements (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        message TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    # ======================================
    # Save Database
    # ======================================

    conn.commit()

    conn.close()
