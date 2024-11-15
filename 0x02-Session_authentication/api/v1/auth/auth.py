#!/usr/bin/env python3
"""Auth class for managing API authentication"""

from typing import List, TypeVar
from flask import request


class Auth:
    """Template class for authentication management"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if a given path requires authentication."""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        normalized_path = path.rstrip('/')

        for excluded_path in excluded_paths:
            normalized_excluded_path = excluded_path.rstrip('/')

            if normalized_excluded_path.endswith('*'):
                if normalized_path.startswith(normalized_excluded_path[:-1]):
                    return False
            elif normalized_path == normalized_excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves the authorization header from a request."""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user based on the request."""
        return None
