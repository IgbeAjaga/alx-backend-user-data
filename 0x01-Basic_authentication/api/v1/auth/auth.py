#!/usr/bin/env python3
""" Auth module
"""

from typing import List
from flask import request, abort, jsonify
from flask_cors import CORS

class Auth:
    """
    Auth class to manage API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for the given path.

        :param path: The path to check.
        :type path: str
        :param excluded_paths: The list of paths that are excluded from authentication.
        :type excluded_paths: List[str]
        :return: True if authentication is required, False otherwise.
        :rtype: bool
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            # If the excluded path ends with "*", check if the path starts with the specified prefix
            if excluded_path.endswith("*"):
                prefix = excluded_path[:-1]
                if path.startswith(prefix):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Extracts the Authorization header from the request.

        :param request: The Flask request object.
        :type request: Request
        :return: The Authorization header value.
        :rtype: str
        """
        if request is None or "Authorization" not in request.headers:
            return None

        return request.headers["Authorization"]

    def current_user(self, request=None) -> 'User':
        """
        Retrieves the User instance for a request.

        :param request: The Flask request object.
        :type request: Request
        :return: The User instance.
        :rtype: User
        """
        return None
