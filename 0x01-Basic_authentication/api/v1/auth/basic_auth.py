#!/usr/bin/env python3
"""auth module for authentication"""


from typing import List, TypeVar
from flask import request
from api.v1.auth.auth import Auth


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
        pass
