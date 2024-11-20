#!/usr/bin/env python3
"""This is the hash password module that takes in
password and hash it
"""

from uuid import uuid4
import bcrypt
from db import DB
from user import User
from bcrypt import hashpw, gensalt
from typing import Optional


def _hash_password(password: str) -> bytes:
    """This method takes in password, hash and reurns
    salted hash
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """This method registers a new email and password
        if the user already esists, a value error message
        is raised
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password.decode('utf-8'))

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login credentials"""
        try:
            stored_hashed_password = user.hashed_password.encode('utf-8')
            input_password = password.encode('utf-8')
            if bcrypt.checkpw(input_password, stored_hashed_password):
                return True
        except NoResultFound:
            pass
        return False

    def _generate_uuid() -> str:
        """This method generates a unique ID"""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> Optional[str]:
        """This function creates a session using the email
        and password
        """
        try:
            user = self._db.find_user_by(email=email)

            session_id = str(uuid4())

            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str):
        """Retrieve a user based on the given session id"""
        if session_id is None:
            return None

        try:
            user = self.__db.find_user_by(session_id=session_id)
            return user
        except (NoResultFoun, InvalidRequestError):
            return None

    def destroy_session(self, user_id: int):
        """Destroy user session by getting their session id
        and setting it to none
        """
        try:
            user = self._db.find_user_by(id=user_id)

            self._db.update_user(user.id, session_id=None)
        except (NoResultFound, InvalidRequestError):
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for user identified
        by their mail
        """
        try:
            uder = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"User with email {email} does not exist")

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ This Method updates the password of user if
        credentials is correct
        """
        user = self._db.find_user_by(reset_token=reset_token)
        if user is None:
            raise ValueError("Invaid reset token")

        hashed_password = _hash_password(password)

        self._db.update_user(
                user.id, hashed_password=hashed_password, reset_token=None
                )
