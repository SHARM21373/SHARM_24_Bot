import os

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
