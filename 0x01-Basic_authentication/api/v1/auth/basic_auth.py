#!/usr/bin/env python3
""" Basic Authentication class for the API
"""
from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """Basic Authentication class that inherits from Auth.
    Currently an empty class, to be implemented later.
    """
    

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extracts the Base64 part from the Authorization header for Basic Authentication"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split("Basic ")[1]
