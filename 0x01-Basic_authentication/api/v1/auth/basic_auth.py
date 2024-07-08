"""auth module for authentication"""


from typing import List, TypeVar
from flask import request
from api.v1.auth.auth import Auth


class Basic_auth(Auth):
    """basic auth authentication"""