#!/usr/bin/env python3
"""auth module"""
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from bcrypt import checkpw, hashpw, gensalt
from user import User


def _hash_password(password: str) -> bytes:
    """hashes a passwrd and returns the value"""
    hashed = hashpw(password.encode("utf-8"), gensalt())
    return hashed


def _generate_uuid() -> str:
    """generates a random uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialises the Auth class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a new user"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        user = self._db.add_user(
            email=email,
            hashed_password=_hash_password(password)
        )
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """checks if a user's credentials are valid for login"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return checkpw(password.encode("utf-8"), user.hashed_password)

    def create_session(self, email: str) -> str:
        """generates a session id for a logged in user"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        user.session_id = session_id
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """gets a user by the session_id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: str) -> User:
        """destroys a session id"""
        try:
            self._db.update_user(user_id=user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """generates a reset token"""
        try:
            token = str(uuid4())
            self._db.update_user(reset_token=token)
            return token
        except ValueError:
            raise ValueError
