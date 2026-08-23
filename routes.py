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
    MAX_BATTERY,
    REFERRAL_REWARD
)
def verify_telegram_init_data(init_data):
    if not init_data:
        return None

    try:
        data = dict(parse_qsl(init_data, keep_blank_values=True))

        received_hash = data.pop("hash", None)

        if not received_hash:
            return None

        data_check_string = "\n".join(
            f"{key}={data[key]}"
            for key in sorted(data)
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
routes = Blueprint("routes", __name__)

# ==========================================
# API STATUS
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

    telegram_id = int(
        telegram_user["id"]
    )

    username = telegram_user.get(
        "username",
        ""
    )

    first_name = telegram_user.get(
        "first_name",
        ""
    )

    conn = get_connection()

    try:

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        ).fetchone()


        # ==================================
        # NEW USER
        # ==================================

        if user is None:

            safe_referrer_id = None


            # ==============================
            # CHECK REFERRER
            # ==============================

            if referrer_id:

                try:

                    candidate_id = int(
                        referrer_id
                    )

                    # নিজের referral link নিষিদ্ধ
                    if candidate_id != telegram_id:

                        referrer = conn.execute(
                            """
                            SELECT telegram_id
                            FROM users
                            WHERE telegram_id = ?
                            """,
                            (candidate_id,)
                        ).fetchone()

                        if referrer:

                            safe_referrer_id = candidate_id

                except (
                    TypeError,
                    ValueError
                ):

                    safe_referrer_id = None


            # ==============================
            # CREATE USER
            # ==============================

            conn.execute(
                """
                INSERT INTO users(
                    telegram_id,
                    username,
                    first_name,
                    balance,
                    battery,
                    max_battery,
                    referred_by
                )
                VALUES(?,?,?,?,?,?,?)
                """,
                (
                    telegram_id,
                    username,
                    first_name,
                    DEFAULT_BALANCE,
                    DEFAULT_BATTERY,
                    MAX_BATTERY,
                    safe_referrer_id
                )
            )


            # ==============================
            # REFERRAL REWARD
            # ==============================

            if safe_referrer_id:

                conn.execute(
                    """
                    UPDATE users
                    SET
                        balance = balance + ?,
                        referrals = referrals + 1
                    WHERE telegram_id = ?
                    """,
                    (
                        REFERRAL_REWARD,
                        safe_referrer_id
                    )
                )

                conn.execute(
                    """
                    UPDATE users
                    SET referral_rewarded = 1
                    WHERE telegram_id = ?
                    """,
                    (telegram_id,)
                )


            conn.commit()


            # ==============================
            # LOAD NEW USER
            # ==============================

            user = conn.execute(
                """
                SELECT *
                FROM users
                WHERE telegram_id = ?
                """,
                (telegram_id,)
            ).fetchone()


        # ==================================
        # EXISTING USER
        # ==================================

        else:

            conn.execute(
                """
                UPDATE users
                SET
                    username = ?,
                    first_name = ?,
                    last_login = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE telegram_id = ?
                """,
                (
                    username,
                    first_name,
                    telegram_id
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


        # ==================================
        # RESPONSE
        # ==================================

        return jsonify({
            "success": True,

            "user": {
                "telegram_id":
                    user["telegram_id"],

                "username":
                    user["username"],

                "first_name":
                    user["first_name"]
            },

            "balance":
                int(user["balance"] or 0),

            "battery":
                int(user["battery"] or 0),

            "max_battery":
                int(user["max_battery"] or 0),

            "tap_power":
                int(user["tap_power"] or 1),

            "mine_level":
                int(user["mine_level"] or 1),

            "referrals":
                int(user["referrals"] or 0)
        })

    except Exception as error:

        conn.rollback()

        print(
            "get_me error:",
            error
        )

        return jsonify({
            "success": False,
            "error": "Database error"
        }), 500

    finally:

        conn.close()

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

    try:

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        ).fetchone()

        if user is None:
            return jsonify({
                "success": False,
                "error": "User not found"
            }), 404

        battery = int(user["battery"] or 0)
        tap_power = int(user["tap_power"] or 1)

        if battery < tap_power:
            return jsonify({
                "success": False,
                "error": "Battery empty"
            })

        new_balance = int(user["balance"]) + tap_power
        new_battery = battery - tap_power

        conn.execute(
            """
            UPDATE users
            SET
                balance = ?,
                battery = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE telegram_id = ?
            """,
            (
                new_balance,
                new_battery,
                telegram_id
            )
        )

        conn.commit()

        return jsonify({
            "success": True,
            "balance": new_balance,
            "battery": new_battery,
            "pending": tap_power
        })

    except Exception as error:

        conn.rollback()

        print("tap error:", error)

        return jsonify({
            "success": False,
            "error": "Database error"
        }), 500

    finally:

        conn.close()
# ==========================================
# REFERRALS
# ==========================================

@routes.post("/api/referrals")
def get_referrals():

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

    try:

        user = conn.execute(
            """
            SELECT telegram_id,
                   referrals,
                   balance
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        ).fetchone()

        if user is None:
            return jsonify({
                "success": False,
                "error": "User not found"
            }), 404

        referral_link = (
            f"https://t.me/SHARM_24_Bot?start={telegram_id}"
        )

        referred_users = conn.execute(
            """
            SELECT
                telegram_id,
                username,
                first_name
            FROM users
            WHERE referred_by = ?
            ORDER BY telegram_id DESC
            """,
            (telegram_id,)
        ).fetchall()

        friends = []

        for row in referred_users:

            friends.append({
                "telegram_id": row["telegram_id"],
                "username": row["username"],
                "first_name": row["first_name"]
            })

        return jsonify({
            "success": True,
            "referral_link": referral_link,
            "referrals": int(user["referrals"] or 0),
            "friends": friends
        })

    except Exception as error:

        conn.rollback()

        print("referrals error:", error)

        return jsonify({
            "success": False,
            "error": "Database error"
        }), 500

    finally:

        conn.close()
