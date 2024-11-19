#!/usr/bin/env python3
""" Auth module for API Authentication
"""
from typing import List, TypeVar
from flask import request

class Auth:
    """ Authentication class for managing API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for the given path"""
        # Return True if the path is None or excluded_paths is None or empty
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        
        # Normalize the paths to ensure slash tolerance
        path = path.rstrip("/")  # Remove trailing slashes from the path
        for excluded_path in excluded_paths:
            if path == excluded_path.rstrip("/"):  # Compare paths without slashes
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the Authorization header value, or None if not present"""
        if request and 'Authorization' in request.headers:
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user from the request, or None if not authenticated"""
        return None  # No user authentication implemented yet
    
    