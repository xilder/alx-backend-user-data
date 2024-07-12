#!/usr/bin/env python3
"""auth module for authentication"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import timedelta, datetime


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth model"""

    def create_session(self, user_id=None):
        """creates a new session"""
        session_id = super().create_session(user_id)
        if type(session_id) != str or not session_id:
            return None
        kwargs = {
            "user_id": user_id,
            "session_id": session_id,
        }
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        retrieves the user_id of the user
        associated with a given id
        """
        try:
            session = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if not session:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = session[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return session[0].user_id

    def destroy_session(self, request=None):
        """destroys the session"""
        session_id = self.session_cookie(request)
        try:
            session  = UserSession.search({"session_id": session_id})
        except Exception:
            return False
        if not session:
            return False
        session[0].remove()
        return True
