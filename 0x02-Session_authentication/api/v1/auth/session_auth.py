#!/usr/bin/env python3
"""Session Authentication module."""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session authentication class."""
    
    # Class attribute for storing session data
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a user ID.
        Args:
            user_id (str): The user ID to associate with the session.
        Returns:
            str: The created session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        
        # Generate a unique Session ID
        session_id = str(uuid.uuid4())
        
        # Store the session ID and its associated user ID
        self.user_id_by_session_id[session_id] = user_id
        
        return session_id
