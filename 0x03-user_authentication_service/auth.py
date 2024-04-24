
#!/usr/bin/env python3
""" Auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """hash user password"""

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))


def _generate_uuid() -> str:
    """generate uuid
    Returns:
        str: new uuid
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """initialize class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user

        Args:
            email (str): user email
            password (str): user password
        Returns:
            User: user object
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except (InvalidRequestError, NoResultFound):
            user = self._db.add_user(email, _hash_password(password))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """check if login is valid

        Args:
            email (str): user email
            password (str): user password

        Returns:
            bool: True if password matches else False
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode(), user.hashed_password)
            return False
        except (InvalidRequestError, NoResultFound):
            return False

    def create_session(self, email: str) -> str:
        """create new session

        Args:
            email (str): user email

        Returns:
            str: new created session id
        """
        try:
            user = self._db.find_user_by(email=email)
            if not user:
                return

            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except (InvalidRequestError, NoResultFound):
            return

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Find user by session id

        Args:
            session_id (str): user session id

        Returns:
            User | None: User object if found else None
        """

        try:
            user = self._db.find_user_by(session_id=session_id)
            if not user:
                return
            if user.session_id is None:
                return
            return user
        except (InvalidRequestError, NoResultFound):
            return

    def destroy_session(self, user_id: int) -> None:
        """Destroy user session

        Args:
            user_id (int): user id
        """

        try:
            self._db.update_user(user_id, session_id=None)
        except (InvalidRequestError, NoResultFound):
            return

    def get_reset_password_token(self, email: str) -> str:
        """Get reset token

        Args:
            email (str): user email
        Returns:
            str: reset token
        """

        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)

            return reset_token
        except (InvalidRequestError, NoResultFound):
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password

        Args:
            reset_token (str): reset token
        """

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                user.id, hashed_password=_hash_password(password),
                reset_token=None
            )
            return
        except (InvalidRequestError, NoResultFound):
            raise ValueError

