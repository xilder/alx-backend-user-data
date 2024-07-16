#!/usr/bin/env python3
"""auth module"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """hashes a passwrd and returns the value"""
    hashed = hashpw(password.encode("utf-8"), gensalt())
    return hashed
