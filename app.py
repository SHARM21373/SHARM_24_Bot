from flask import Flask, jsonify

from database import init_db
from routes import routes

app = Flask(__name__)


app = Flask(__name__)

init_db()
app.register_blueprint(routes)

_bot_started = False
_bot_lock = threading.Lock()


def start_bot_in_background():
    global _bot_started

    with _bot_lock:
        if _bot_started:
            return

        _bot_started = True

    thread = threading.Thread(
        target=start_bot,
        name="telegram-bot",
        daemon=True
    )

    thread.start()


start_bot_in_background()


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "app": "SHARM TAP",
        "version": "1.0.0"
    })


@app.route("/health")
def health():
    return jsonify({
        "success": True
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
