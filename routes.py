from flask import Blueprint, jsonify

routes = Blueprint("routes", __name__)


@routes.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "success": True,
        "message": "SHARM TAP API is running",
        "version": "2.0.0"
    })


@routes.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "status": "healthy"
    })
