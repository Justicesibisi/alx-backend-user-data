#!/usr/bin/env python3
"""Session Authentication View"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from api.v1.app import auth


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_auth_logout():
    """DELETE /api/v1/auth_session/logout
    Handles user logout by destroying the session.
    """
    # Call the destroy_session method
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200

