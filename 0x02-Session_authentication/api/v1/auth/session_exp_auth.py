#!/usr/bin/env python3
"""auth module for authentication"""
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    """Session Expiration Class"""
    def __init__(self):
        """initialises this class"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """creates a new session ID for a user"""
        session_id = super().create_session(user_id)
        if not session_id or type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the user registered with a session"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if "created_at" not in session_dict:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = session_dict["created_at"] + time_span
        if exp_time < cur_time:
            return None
        return session_dict["user_id"]
