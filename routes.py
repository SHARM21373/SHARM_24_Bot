import os
import hmac
import hashlib
import json
from urllib.parse import parse_qsl

from flask import Blueprint, jsonify, request

from database import get_connection


routes = Blueprint("routes", __name__)


BOT_TOKEN = os.environ.get("BOT_TOKEN")

MAX_ENERGY = 1500
POINT_PER_TAP = 1
PROCESSING_SECONDS = 3


# =========================================================
# Telegram Mini App initData verification
# =========================================================

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
            f"{key}={value}"
            for key, value in sorted(data.items())
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

        user_data = data.get("user")

        if not user_data:
            return None

        return json.loads(user_data)

    except Exception:
        return None


# =========================================================
# Status
# =========================================================

@routes.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "success": True,
        "message": "SHARM TAP API is running",
        "version": "3.0.0"
    })


@routes.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "status": "healthy"
    })


# =========================================================
# Get / create Telegram user
# =========================================================

@routes.route("/api/me", methods=["POST"])
def get_me():

    body = request.get_json(silent=True) or {}

    init_data = body.get("initData", "")

    telegram_user = verify_telegram_init_data(init_data)

    if not telegram_user:
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
        SELECT
            telegram_id,
            username,
            first_name,
            coins,
            energy,
            referrals
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    ).fetchone()

    if user is None:

        conn.execute(
            """
            INSERT INTO users (
                telegram_id,
                username,
                first_name,
                coins,
                energy,
                referrals
            )
            VALUES (?, ?, ?, 0, ?, 0)
            """,
            (
                telegram_id,
                username,
                first_name,
                MAX_ENERGY
            )
        )

        conn.commit()

        user = conn.execute(
            """
            SELECT
                telegram_id,
                username,
                first_name,
                coins,
                energy,
                referrals
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        ).fetchone()

    else:

        # Existing users: don't suddenly reset their balance.
        # Only update profile information.
        conn.execute(
            """
            UPDATE users
            SET username = ?, first_name = ?
            WHERE telegram_id = ?
            """,
            (
                username,
                first_name,
                telegram_id
            )
        )

        conn.commit()

    conn.close()

    return jsonify({
        "success": True,
        "user": {
            "telegram_id": user["telegram_id"],
            "username": user["username"],
            "first_name": user["first_name"]
        },
        "balance": int(user["coins"] or 0),
        "battery": int(user["energy"] or 0),
        "max_battery": MAX_ENERGY,
        "referrals": int(user["referrals"] or 0)
    })


# =========================================================
# TAP
# =========================================================

@routes.route("/api/tap", methods=["POST"])
def tap():

    body = request.get_json(silent=True) or {}

    init_data = body.get("initData", "")

    telegram_user = verify_telegram_init_data(init_data)

    if not telegram_user:
        return jsonify({
            "success": False,
            "error": "Invalid Telegram session"
        }), 401

    telegram_id = int(telegram_user["id"])

    conn = get_connection()

    user = conn.execute(
        """
        SELECT coins, energy
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

    balance = int(user["coins"] or 0)
    energy = int(user["energy"] or 0)

    if energy <= 0:
        conn.close()

        return jsonify({
            "success": False,
            "error": "Battery empty",
            "balance": balance,
            "battery": 0
        }), 400

    # One valid tap:
    # Battery -1
    # Coin +1
    new_energy = energy - 1
    new_balance = balance + POINT_PER_TAP

    conn.execute(
        """
        UPDATE users
        SET coins = ?, energy = ?
        WHERE telegram_id = ?
        """,
        (
            new_balance,
            new_energy,
            telegram_id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "added": POINT_PER_TAP,
        "balance": new_balance,
        "battery": new_energy,
        "processing_seconds": PROCESSING_SECONDS
    })
