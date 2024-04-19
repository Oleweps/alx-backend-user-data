#!/usr/bin/env python3
""" Session token expiration module """

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Expire class"""

    def __init__(self):
        """ initialize class """
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """ create new session """

        session_id = super().create_session(user_id)
        if session_id is None:
            return

        sesssion_data = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = sesssion_data

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ get session id """

        session_data = self.user_id_by_session_id.get(session_id)
        if session_id is None or not session_data:
            return

        user_id = session_data.get("user_id")
        if self.session_duration == 0:
            return user_id

        created_at = session_data.get("created_at")
        if created_at is None:
            return

        old_date = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > old_date:
            return

        return user_id
