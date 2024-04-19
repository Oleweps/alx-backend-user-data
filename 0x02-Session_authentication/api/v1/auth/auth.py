#!/usr/bin/env python3
""" Auth module
"""
from flask import request
from typing import TypeVar, List
import re
import os


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        for val in excluded_paths:
            if val.endswith("*"):
                val = val.replace("*", ".*")
                if re.match(re.compile(val), path):
                    return False

            if val.rstrip("/") == path.rstrip("/"):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""

        if request is None:
            return

        auth_header = request.headers.get("Authorization")

        if auth_header is None:
            return

        return auth_header

    def current_user(self, request=None) -> TypeVar("User"):
        """get current user"""
        return

    def session_cookie(self, request=None) -> str:
        """ create a session cookie """
        if request is None:
            return

        return request.cookies.get(os.getenv('SESSION_NAME'))
