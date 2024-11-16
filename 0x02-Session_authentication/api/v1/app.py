#!/usr/bin/env python3
"""API module."""
from os import getenv
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Determine the authentication type
auth = None
auth_type = getenv("AUTH_TYPE", "auth")
if auth_type == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()

# Excluded paths
EXCLUDED_PATHS = [
    "/api/v1/status/",
    "/api/v1/unauthorized/",
    "/api/v1/forbidden/",
    "/api/v1/auth_session/login/"
]

@app.before_request
def before_request():
    """
    Method to handle authentication before each request.
    """
    if auth is None:
        return

    # Exclude specific paths
    if not auth.require_auth(request.path, EXCLUDED_PATHS):
        return

    # Check if Authorization header or session cookie is provided
    if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
        abort(401)

@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 unauthorized errors."""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    """Handle 403 forbidden errors."""
    return jsonify({"error": "Forbidden"}), 403

@app.errorhandler(404)
def not_found(error):
    """Handle 404 not found errors."""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", 5000))
    app.run(host=host, port=port)

