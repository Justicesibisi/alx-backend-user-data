#!/usr/bin/env python3
"""SessionAuth module for handling session-based authentication."""
from api.v1.auth.auth import Auth
from models.user import User

class SessionAuth(Auth):
    """SessionAuth class for managing user sessions."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID for a user."""
        if user_id is None or not isinstance(user_id, str):
            return None
        import uuid
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve a User ID by session ID."""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieve the User instance associated with the session ID.
        """
        # Get the session ID from the session cookie
        session_id = self.session_cookie(request)
        if not session_id:
            return None

        # Get the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        # Retrieve the User instance from the database
        try:
            return User.get(user_id)
        except Exception:
            return None

