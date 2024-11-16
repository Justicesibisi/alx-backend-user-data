#!/usr/bin/env python3
"""Session Authentication"""

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session authentication class"""

    user_id_by_session_id = {}

    def destroy_session(self, request=None):
        """Destroys a user session/logout"""
        if request is None:
            return False

        # Retrieve session ID from the cookie
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        # Retrieve user ID associated with session ID
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        # Delete the session ID from the dictionary
        del self.user_id_by_session_id[session_id]
        return True

