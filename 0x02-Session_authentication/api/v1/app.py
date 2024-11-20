#!/usr/bin/env python3
"""API app module."""
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from os import getenv
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
CORS(app)

auth = BasicAuth()

@app.before_request
def before_request():
    """Executes before every request."""
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized', '/api/v1/forbidden']
    if not auth.require_auth(request.path, excluded_paths):
        return
    if not auth.authorization_header(request):
        abort(401)
    request.current_user = auth.current_user(request)

@app.route('/api/v1/status', methods=['GET'], strict_slashes=False)
def status():
    """Status endpoint."""
    return jsonify({"status": "OK"})

@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors."""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

