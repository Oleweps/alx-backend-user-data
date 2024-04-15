#!/usr/bin/env python3
""" Basic auth module
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic auth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """get Base64 part of the Authorization
        header for a Basic Authentication
        """
        start = "Basic "

        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or start not in authorization_header
        ):
            return

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Basic - Base64 decode"""

        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return

        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode("utf-8")
        except Exception as e:
            return

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Extract user credentials"""
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or ":" not in decoded_base64_authorization_header
        ):
            return (None, None)

        decoded = decoded_base64_authorization_header.split(":")
        if len(decoded) > 2:
            return (decoded[0], ":".join(decoded[1:]))

        return tuple(decoded)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """get User instance based on his email and password."""
        if (
            user_email is None
            or not isinstance(user_email, str)
            or user_pwd is None
            or not isinstance(user_pwd, str)
        ):
            return

        try:
            users = User.search({'email': user_email})
        except Exception as e:
            users = []

        if len(users) == 0:
            return

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return

    def current_user(self, request=None) -> TypeVar('User'):
        """ get current user """

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return

        base64_ = self.extract_base64_authorization_header(auth_header)
        if base64_ is None:
            return

        decoded_base64 = self.decode_base64_authorization_header(base64_)
        if decoded_base64 is None:
            return

        user_creds = self.extract_user_credentials(decoded_base64)
        if user_creds == (None, None):
            return

        return self.user_object_from_credentials(user_creds[0], user_creds[1])
