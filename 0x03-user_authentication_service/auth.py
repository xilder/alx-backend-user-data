#!/usr/bin/env python3
"""auth module"""
from typing import Union
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from bcrypt import hashpw, gensalt
from user import User


def _hash_password(password: str) -> bytes:
    """hashes a passwrd and returns the value"""
    hashed = hashpw(password.encode("utf-8"), gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialises the Auth class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[User | None]:
        """registers a new user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError(f"User {email} already exists")
