#!/usr/bin/env python3
""" Auth module for API Authentication
"""
from typing import List, TypeVar
from flask import request
import base64
from models.user import User
from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """ Basic Authentication class that inherits from Auth
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header"""
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Returns the decoded value of a Base64 string"""
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return decoded_base64_authorization_header.split(":", 1)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns a User instance based on email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Use User.search to find the user by email
        users = User.search({'email': user_email})
        if not users:
            return None
        
        user = users[0]  # Assuming the email is unique, take the first match

        # Verify password
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user based on the request"""
        if request is None:
            return None

        # Retrieve the Authorization header
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None

        # Extract the Base64 part
        base64_authorization_header = self.extract_base64_authorization_header(authorization_header)
        if base64_authorization_header is None:
            return None

        # Decode the Base64 part
        decoded_base64_authorization_header = self.decode_base64_authorization_header(base64_authorization_header)
        if decoded_base64_authorization_header is None:
            return None

        # Extract the user credentials
        user_email, user_pwd = self.extract_user_credentials(decoded_base64_authorization_header)
        if user_email is None or user_pwd is None:
            return None

        # Retrieve the user object based on the credentials
        return self.user_object_from_credentials(user_email, user_pwd)

