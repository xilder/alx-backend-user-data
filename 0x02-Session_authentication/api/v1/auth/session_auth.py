#!/usr/bin/env python3
"""auth module for authentication"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """session auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None):
        """creates a Session ID for a user_id"""
        if  user_id is None:
            return None

        if type(user_id) != str:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
