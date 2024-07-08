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
        if not path or not excluded_paths:
            return True
        if path in excluded_paths:
            return False
        for excluded_path in excluded_paths:
            if excluded_path.startswith(path):
                return False
            elif path.startswith(excluded_path):
                return False
            elif excluded_path[-1] == "*":
                if path.startswith(excluded_path[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """"returns None"""
        return None
