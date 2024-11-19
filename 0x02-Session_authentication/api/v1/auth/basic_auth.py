import base64
from flask import request

class BasicAuth:
    """Handles Basic Authentication logic"""
    
    def require_auth(self, path, excluded_paths):
        """Returns True if authentication is required for the path"""
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request):
        """Extracts the authorization header from the request"""
        return request.headers.get("Authorization")

    def current_user(self, request):
        """Returns the current user based on the authorization header"""
        auth_header = self.authorization_header(request)
        if not auth_header or not auth_header.startswith("Basic "):
            return None
        
        try:
            # Decode the Base64 credentials
            encoded_credentials = auth_header.split(" ")[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
            username, password = decoded_credentials.split(":")
            
            # Example check for username/password (replace with real logic)
            if self.verify_credentials(username, password):
                return username
            return None
        except Exception:
            return None

    def verify_credentials(self, username, password):
        """Verify the provided username and password (replace with real authentication)"""
        valid_users = {
            "admin": "password123",
            "user1": "password456"
        }
        return valid_users.get(username) == password

