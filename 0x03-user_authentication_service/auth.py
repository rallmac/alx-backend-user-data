#!/usr/bin/env python3
"""This is the hash password module that takes in
password and hash it
"""

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
        except Exception:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password.decode('utf-8'))
            return user
