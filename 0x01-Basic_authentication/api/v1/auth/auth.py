#!/usr/bin/env python3
"""Authentication module for the API.
"""

import re
from typing import List, TypeVar
from flask import request

class Auth:
    """Handles authentication for the API.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authentication.

        Args:
            path (str): The path to be checked.
            excluded_paths (List[str]): List of paths that do not require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is not None and excluded_paths is not None:
            for excluded_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if excluded_path[-1] == '*':
                    pattern = '{}.*'.format(excluded_path[0:-1])
                elif excluded_path[-1] == '/':
                    pattern = '{}/*'.format(excluded_path[0:-1])
                else:
                    pattern = '{}/*'.format(excluded_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Gets the authorization header field from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The value of the Authorization header, or None if not present.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user from the request.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): The current user, or None if not available.
        """
        return None
