#!/usr/bin/env python3
"""SessionAuth module for managing session authentication"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """SessionAuth class that handles session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a given user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid())

        self.user_id_by_session_id[session_id] = user_id

        return session_id
