#!/usr/bin/env python3
"""auth module for authentication"""


from typing import List, TypeVar
from flask import request
from api.v1.auth.auth import Auth
import base64
from models.user import User
from models.base import Base


class BasicAuth(Auth):
    """basic auth authentication"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str
    ) -> str:
        """returns the  base64 part of the Authorization header"""
        if not authorization_header:
            return None

        if type(authorization_header) != str:
            return None

        if not authorization_header.startswith("Basic "):
            return None

        auth_params = authorization_header.split()
        auth = auth_params[1]

        return auth

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str,
    ) -> str:
        """decodes b64 encoded strings"""
        if base64_authorization_header is None:
            return None

        if type(base64_authorization_header) != str:
            return None

        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        """extracts essential info from the argument passed"""
        if decoded_base64_authorization_header is None:
            return (None, None)

        if type(decoded_base64_authorization_header) != str:
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        params = decoded_base64_authorization_header.split(':')
        email, password = params

        return (email, password)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
    ) -> TypeVar('User'):
        """returns a user if found"""
        if user_email is None or type(user_email) != str:
            return None

        if user_pwd is None or type(user_pwd) != str:
            return None

        users = User.search()
        try:
            if not users or users == []:
                return None

            for user in users:
                if user.is_valid_password(user_pwd):
                    return user

            return None
        except Exception:
            return None
