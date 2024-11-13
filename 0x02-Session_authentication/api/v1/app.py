#!/usr/bin/env python3
"""
Main module for the API
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)

# Registering the blueprint
app.register_blueprint(app_views)

# Enabling CORS
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Create an instance of Auth or BasicAuth depending on the environment variable
auth = None
auth_type = getenv("AUTH_TYPE")

if auth_type == "basic_auth":
    auth = BasicAuth()  # Use BasicAuth if AUTH_TYPE is 'basic_auth'
else:
    auth = Auth()  # Default to Auth if AUTH_TYPE is not 'basic_auth'

@app.before_request
def before_request():
    """Filter each request and check for authentication"""
    # If authentication is not required, skip the validation
    if auth is None:
        return
    
    # List of paths that don't require authentication
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    
    # Check if the path requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        return

    # If no Authorization header is present, raise 401 Unauthorized
    if auth.authorization_header(request) is None:
        abort(401)

    # Set current user in the request context
    request.current_user = auth.current_user(request)

    # If the current user is not authenticated, raise 403 Forbidden
    if request.current_user is None:
        abort(403)

@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """Return a 401 Unauthorized error"""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden_error(error) -> str:
    """Return a 403 Forbidden error"""
    return jsonify({"error": "Forbidden"}), 403

@app.errorhandler(404)
def not_found_error(error) -> str:
    """Return a 404 Not Found error"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
