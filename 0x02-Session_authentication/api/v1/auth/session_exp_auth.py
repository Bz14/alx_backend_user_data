#!/usr/bin/env python3
""" Module of Index views """

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ SessionAuth class """

    def __init__(self):
        """ Constructor """
        super().__init__()
        self.session_duration = int(os.getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """ create session """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ user_id_for_session_id """
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if session_dict.get('created_at') is None:
            return None
        if (session_dict.get('created_at') +
                timedelta(seconds=self.session_duration) < datetime.now()):
            return None
        return session_dict.get('user_id')
