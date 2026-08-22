import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from telegram import Update

from database import init_db
from routes import routes
from bot import application


app = Flask(__name__)

# Allow requests from your GitHub Pages Mini App
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://sharm21373.github.io"
            ]
        }
    }
)

# Initialize database
init_db()

# Register API routes
app.register_blueprint(routes)


@app.get("/")
def home():
    return jsonify({
        "status": "online",
        "app": "SHARM TAP",
        "version": "3.0.0"
    })


@app.get("/health")
def health():
    return jsonify({
        "success": True
    })


@app.post("/webhook")
async def webhook():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "Invalid Telegram update"
        }), 400

    update = Update.de_json(
        data,
        application.bot
    )

    if not application.initialized:
        await application.initialize()

    if not application.running:
        await application.start()

    await application.process_update(update)

    return jsonify({
        "success": True
    })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
