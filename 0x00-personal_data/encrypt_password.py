#!/usr/bin/env python3
"""Module for password hashing using bcrypt."""


import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt with automatic salting"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates a password against its hashed version."""
    return bcrypt.checkpw(password.encode(), hashed_password)
