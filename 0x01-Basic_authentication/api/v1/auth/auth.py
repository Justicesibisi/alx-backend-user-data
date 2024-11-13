# api/v1/auth/auth.py
from typing import List, TypeVar
from flask import request

class Auth:
    """ Authentication class for managing API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for the given path"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        
        # Normalize paths to ensure slash tolerance
        path = path.rstrip("/")
        for excluded_path in excluded_paths:
            if path == excluded_path.rstrip("/"):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the Authorization header value, or None if not present"""
        if request is None:
            return None
        if 'Authorization' in request.headers:
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user from the request, or None if not authenticated"""
        return None  # No user authentication implemented yet
