from flask import Flask, request, jsonify

from database import init_db
from bot import application

app = Flask(__name__)

init_db()


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "app": "SHARM TAP",
        "version": "2.0.0"
    })


@app.route("/health")
def health():
    return jsonify({
        "success": True
    })


@app.post("/webhook")
async def webhook():
    data = request.get_json(force=True)

    await application.initialize()

    update = application.update_queue
    # এখানে পরের ধাপে Telegram Update প্রসেসিং যোগ হবে

    return jsonify({
        "success": True
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
