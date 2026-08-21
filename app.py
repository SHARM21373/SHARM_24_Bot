from flask import Flask, jsonify
from database import init_db
from routes import routes

app = Flask(__name__)

# Database তৈরি
init_db()

# Routes যুক্ত করা
app.register_blueprint(routes)

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "app": "SHARM TAP",
        "version": "1.0.0",
        "message": "Backend is running successfully!"
    })

@app.route("/health")
def health():
    return jsonify({
        "success": True,
        "message": "Server is healthy"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
