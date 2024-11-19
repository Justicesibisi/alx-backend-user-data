#!/usr/bin/env python3
"""Auth module for authentication."""
from flask import request
from os import getenv


class Auth:
    """Auth class for managing authentication."""

    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """Determine if a given path requires authentication."""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        for exc_path in excluded_paths:
            if exc_path.endswith('/'):
                if path.startswith(exc_path[:-1]):
                    return False
            elif path == exc_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return the authorization header from a request."""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None):
        """Return the current user (to be implemented in derived classes)."""
        return None

    def session_cookie(self, request=None):
        """
        Retrieve the session cookie value from the request.

        Args:
            request (Request): The Flask request object.
        Returns:
            str: The value of the session cookie, or None if not found.
        """
        if request is None:
            return None
        
        # Get the cookie name from the environment variable
        session_name = getenv("SESSION_NAME")
        if not session_name:
            return None
        
        # Retrieve and return the cookie value
        return request.cookies.get(session_name)
    
