#!/usr/bin/env python3
"""auth module for authentication"""


from typing import List, TypeVar
from flask import request


class Auth:
    """auth class"""
    def require_auth(
            self,
            path: str,
            excluded_paths: List[str]
        ) -> bool:
        """returns False"""
        return False


    def authorization_header(self, request=None) -> str:
        """returns None"""
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """"returns None"""
        return None
