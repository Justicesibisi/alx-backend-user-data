#!/usr/bin/env python3
"""Session DB authentication module."""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class SessionDBAuth(SessionExpAuth):
    """Session authentication using a database."""

    def __init__(self):
        """Initializes session authentication with database storage."""
        super().__init__()
        self.engine = create_engine('sqlite:///sessions.db')  # Adjust this to your DB URI
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_session(self, user_id=None):
        """Create a session and store it in the database."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # Store session in the database
        user_session = UserSession(user_id=user_id, session_id=session_id)
        self.session.add(user_session)
        self.session.commit()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return user ID for the given session ID."""
        if session_id is None:
            return None

        # Query the session in the database
        user_session = self.session.query(UserSession).filter_by(session_id=session_id).first()
        if user_session is None:
            return None

        # Check expiration
        return super().user_id_for_session_id(session_id)

    def destroy_session(self, request=None):
        """Destroy a session from the database."""
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_session = self.session.query(UserSession).filter_by(session_id=session_id).first()
        if user_session:
            self.session.delete(user_session)
            self.session.commit()
            return True
        return False


