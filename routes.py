import hmac
import hashlib
import json
from urllib.parse import parse_qsl

from flask import Blueprint, jsonify, request

from database import get_connection
from config import (
    BOT_TOKEN,
    APP_NAME,
    APP_VERSION,
    DEFAULT_BALANCE,
    DEFAULT_BATTERY,
    MAX_BATTERY
)

routes = Blueprint("routes", __name__)

# ==========================================
# Telegram Mini App Authentication
# ==========================================

def verify_telegram_init_data(init_data):

    if not BOT_TOKEN or not init_data:
        return None

    try:

        data = dict(
            parse_qsl(
                init_data,
                keep_blank_values=True
            )
        )

        received_hash = data.pop("hash", None)

        if not received_hash:
            return None

        data_check_string = "\n".join(
            f"{k}={v}"
            for k, v in sorted(data.items())
        )

        secret_key = hmac.new(
            b"WebAppData",
            BOT_TOKEN.encode(),
            hashlib.sha256
        ).digest()

        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(
            calculated_hash,
            received_hash
        ):
            return None

        return json.loads(data["user"])

    except Exception:
        return None


# ==========================================
# Health
# ==========================================

@routes.get("/health")
def health():

    return jsonify({
        "success": True,
        "status": "healthy"
    })


# ==========================================
# API Status
# ==========================================

@routes.get("/api/status")
def status():

    return jsonify({
        "success": True,
        "app": APP_NAME,
        "version": APP_VERSION
    })


# ==========================================
# Current User
# ==========================================

@routes.post("/api/me")
def get_me():

    body = request.get_json(silent=True) or {}
    
    referrer_id = body.get("referrer_id")

    telegram_user = verify_telegram_init_data(
        body.get("initData", "")
    )

    if telegram_user is None:

        return jsonify({
            "success": False,
            "error": "Invalid Telegram session"
        }), 401

    telegram_id = int(telegram_user["id"])
    username = telegram_user.get("username", "")
    first_name = telegram_user.get("first_name", "")

    conn = get_connection()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    ).fetchone()

    if user is None:

        conn.execute(
            """
            INSERT INTO users(
                telegram_id,
                username,
                first_name,
                balance,
                battery,
                max_battery
            )
            VALUES(?,?,?,?,?,?)
            """,
            (
                telegram_id,
                username,
                first_name,
                DEFAULT_BALANCE,
                DEFAULT_BATTERY,
                MAX_BATTERY
            )
        )

        conn.commit()

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        ).fetchone()

    conn.close()

    return jsonify({
        "success": True,
        "user": {
            "telegram_id": user["telegram_id"],
            "username": user["username"],
            "first_name": user["first_name"]
        },
        "balance": user["balance"],
        "battery": user["battery"],
        "max_battery": user["max_battery"],
        "tap_power": user["tap_power"],
        "mine_level": user["mine_level"],
        "referrals": user["referrals"]
    })
    # ==========================================
# TAP
# ==========================================

@routes.post("/api/tap")
def tap():

    body = request.get_json(silent=True) or {}

    telegram_user = verify_telegram_init_data(
        body.get("initData", "")
    )

    if telegram_user is None:

        return jsonify({
            "success": False,
            "error": "Invalid Telegram session"
        }), 401

    telegram_id = int(telegram_user["id"])

    conn = get_connection()

    user = conn.execute(
        """
        SELECT
            balance,
            battery,
            max_battery,
            tap_power
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    ).fetchone()

    if user is None:

        conn.close()

        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    balance = int(user["balance"])
    battery = int(user["battery"])
    tap_power = int(user["tap_power"])

    if battery < tap_power:

        conn.close()

        return jsonify({
            "success": False,
            "error": "Battery empty",
            "balance": balance,
            "battery": battery
        }), 400

    new_balance = balance + tap_power
    new_battery = battery - tap_power

    conn.execute(
        """
        UPDATE users
        SET
            balance = ?,
            battery = ?,
            last_login = CURRENT_TIMESTAMP
        WHERE telegram_id = ?
        """,
        (
            new_balance,
            new_battery,
            telegram_id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "added": tap_power,
        "balance": new_balance,
        "battery": new_battery
    })
# ==========================================
# REFERRAL
# ==========================================

@routes.post("/api/referral")
def referral():

    body = request.get_json(silent=True) or {}

    telegram_user = verify_telegram_init_data(
        body.get("initData", "")
    )

    if telegram_user is None:
        return jsonify({
            "success": False,
            "error": "Invalid Telegram session"
        }), 401

    telegram_id = int(telegram_user["id"])

    conn = get_connection()

    user = conn.execute(
        """
        SELECT telegram_id, referrals
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    ).fetchone()

    if user is None:
        conn.close()

        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    referrals = int(user["referrals"] or 0)

    conn.close()

    return jsonify({
        "success": True,
        "referrals": referrals
    })


# ==========================================
# LEADERBOARD
# ==========================================

@routes.get("/api/leaderboard")
def leaderboard():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            telegram_id,
            username,
            first_name,
            balance
        FROM users
        ORDER BY balance DESC
        LIMIT 50
        """
    ).fetchall()

    leaderboard_data = []

    for position, row in enumerate(rows, start=1):

        display_name = (
            row["username"]
            or row["first_name"]
            or "Telegram User"
        )

        leaderboard_data.append({
            "rank": position,
            "telegram_id": row["telegram_id"],
            "username": display_name,
            "balance": int(row["balance"] or 0)
        })

    conn.close()

    return jsonify({
        "success": True,
        "leaderboard": leaderboard_data
    })


# ==========================================
# DAILY REWARD
# ==========================================

@routes.post("/api/daily/claim")
def claim_daily_reward():

    body = request.get_json(silent=True) or {}

    telegram_user = verify_telegram_init_data(
        body.get("initData", "")
    )

    if telegram_user is None:
        return jsonify({
            "success": False,
            "error": "Invalid Telegram session"
        }), 401

    telegram_id = int(telegram_user["id"])

    conn = get_connection()

    user = conn.execute(
        """
        SELECT balance
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    ).fetchone()

    if user is None:
        conn.close()

        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    # Base daily reward.
    # পরে চাইলে settings/table থেকে পরিবর্তন করা যাবে।
    reward = 100

    conn.execute(
        """
        UPDATE users
        SET balance = balance + ?
        WHERE telegram_id = ?
        """,
        (
            reward,
            telegram_id
        )
    )

    conn.commit()

    updated_user = conn.execute(
        """
        SELECT balance
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    ).fetchone()

    conn.close()

    return jsonify({
        "success": True,
        "reward": reward,
        "balance": int(updated_user["balance"] or 0)
    })


# ==========================================
# SETTINGS
# ==========================================

@routes.get("/api/settings")
def settings():

    return jsonify({
        "success": True,
        "settings": {
            "app_name": APP_NAME,
            "version": APP_VERSION,
            "tap_enabled": True,
            "referral_enabled": True,
            "leaderboard_enabled": True,
            "daily_reward_enabled": True,
            "shop_enabled": True,
            "wallet_connect": False,
            "airdrop": "coming_soon"
        }
    })


# ==========================================
# ANNOUNCEMENTS
# ==========================================

@routes.get("/api/announcements")
def announcements():

    conn = get_connection()

    try:

        rows = conn.execute(
            """
            SELECT *
            FROM announcements
            ORDER BY id DESC
            LIMIT 20
            """
        ).fetchall()

        data = []

        for row in rows:

            item = {}

            for key in row.keys():
                item[key] = row[key]

            data.append(item)

        conn.close()

        return jsonify({
            "success": True,
            "announcements": data
        })

    except Exception:

        conn.close()

        return jsonify({
            "success": True,
            "announcements": []
        })
