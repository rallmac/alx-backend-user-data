#!/usr/bin/env python3
"""Auth class for managing API authentication"""

from typing import List, TypeVar
from flask import request


class Auth:
    """Template class for authentication management"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if a given path requires authentication
        currently returns false as a placeholder
        """
        if path is None:
            return True
        if not excluded_paths:
            return True

        normalized_path = path if path.endswith('/') else path + '/'
        normalized_excluded_paths = []
        for p in excluded_paths:
            normalized_excluded_paths.append(p if p.endswith('/') else p + '/')
        return normalized_path not in normalized_excluded_paths

    def authorization_header(self, request=None) -> str:
        """Retrieves the authorization header from a request
        currently returns None as a placeholder
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user based on the request
        currently returns None as a placeholder
        """
        return None
