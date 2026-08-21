from flask import Flask, jsonify

from api.database import init_db
from api.routes import routes

app = Flask(__name__)

init_db()
app.register_blueprint(routes)

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
    app.run(host="0.0.0.0", port=5000)
