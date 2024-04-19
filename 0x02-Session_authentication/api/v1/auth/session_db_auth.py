#!/usr/bin/env python3
""" New authentication class """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import timedelta, datetime
import os


class SessionDBAuth(SessionExpAuth):
    """ SessionDbAuth class """

    def create_session(self, user_id=None):
        """ create new session """

        session_id = super().create_session(user_id)
        if session_id is None:
            return

        data = {"user_id": user_id, "session_id": session_id}
        user = UserSession(**data)
        user.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ get user id using session"""
        if session_id is None:
            return

        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception as e:
            sessions = []

        if len(sessions) == 0:
            return

        session = sessions[0]
        user_id = session.user_id
        if self.session_duration == 0:
            return user_id

        created_at = session.created_at
        if created_at is None:
            return

        old_date = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > old_date:
            return

        return user_id

    def destroy_session(self, request=None):
        """ destroy session """
        if request is None:
            return False

        session_id = request.cookies.get(os.getenv("SESSION_NAME"))
        if not session_id:
            return False

        sessions = UserSession.search({"session_id": session_id})
        if len(sessions) == 0:
            return False

        del self.user_id_by_session_id[session_id]
        sessions[0].remove()

        return True
