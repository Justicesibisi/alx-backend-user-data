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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the User ID based on a Session ID.
        Args:
            session_id (str): The session ID to look up.
        Returns:
            str: The associated User ID, or None if session_id is invalid or not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        
        # Use .get() to retrieve the user ID
        return self.user_id_by_session_id.get(session_id)
