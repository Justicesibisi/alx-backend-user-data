# api/v1/app.py
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from flask_cors import CORS
from api.v1.auth.auth import Auth  # Import the Auth class

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth to None
auth = None

# Check the AUTH_TYPE environment variable to initialize the correct authentication class
auth_type = getenv("AUTH_TYPE")
if auth_type == "auth":
    auth = Auth()

@app.before_request
def before_request():
    """Before request handler for API authentication"""
    if auth is None:
        return  # Do nothing if no authentication is defined

    # List of routes that don't require authentication
    excluded_routes = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

    # If the current path is not excluded from authentication checks
    if not auth.require_auth(request.path, excluded_routes):
        return  # No authentication needed for this request

    # Check if the Authorization header is present
    if auth.authorization_header(request) is None:
        abort(401)  # Unauthorized if no header

    # Check if the current user is authenticated
    if auth.current_user(request) is None:
        abort(403)  # Forbidden if no user is found

@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden_error(error) -> str:
    """ Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
