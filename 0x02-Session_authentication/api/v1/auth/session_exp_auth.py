#!/usr/bin/env python3
"""
SessionExpAuth module for session expiration.
"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class to manage session expiration.
    """

    def __init__(self):
        """Initialize with session duration."""
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
            logging.debug(f"Session duration set to {self.session_duration} seconds")
        except ValueError:
            self.session_duration = 0
            logging.error("Invalid SESSION_DURATION value, defaulting to 0 seconds")

    def create_session(self, user_id=None):
        """Create a session with expiration."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # Add a session dictionary with expiration details
        session_info = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_info
        logging.debug(f"Session created with ID {session_id} for user {user_id} at {session_info['created_at']}")
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return user_id if session is valid."""
        if session_id is None:
            return None

        session_info = self.user_id_by_session_id.get(session_id)
        if session_info is None:
            logging.warning(f"Session ID {session_id} not found in user_id_by_session_id.")
            return None

        if self.session_duration <= 0:
            logging.debug(f"Session ID {session_id} duration is 0 or less, no expiration check.")
            return session_info.get("user_id")

        created_at = session_info.get("created_at")
        if created_at is None:
            logging.warning(f"Session ID {session_id} has no 'created_at' key.")
            return None

        # Check if the session has expired
        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            logging.warning(f"Session ID {session_id} has expired.")
            return None

        logging.debug(f"Session ID {session_id} is valid, returning user_id.")
        return session_info.get("user_id")


