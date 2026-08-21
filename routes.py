from flask import Blueprint, jsonify

routes = Blueprint("routes", __name__)

@routes.route("/api/status")
def status():
    return jsonify({
        "success": True,
        "message": "SHARM TAP API is running"
    })
