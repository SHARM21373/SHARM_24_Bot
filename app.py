from flask import Flask, jsonify

app = Flask(__name__)

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
