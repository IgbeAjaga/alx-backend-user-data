#!/usr/bin/env python3
"""Basic authentication
"""


import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class inherits from Auth.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic Auth

        :param authorization_header: The Authorization header value.
        :type authorization_header: str
        :return: The Base64 part.
        :rtype: str
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split("Basic ", 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 Authorization header.

        :param base64_authorization_header: The Base64 Authorization header.
        :type base64_authorization_header: str
        :return: The decoded value.
        :rtype: str
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user credentials from the decoded Base64 Authorization header.

        :param decoded_base64_authorization_header: The decoded Base64 AH
        :type decoded_base64_authorization_header: str
        :return: User email and password tuple.
        :rtype: (str, str)
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> 'User':
        """
        Retrieves the User instance based on email and password.

        :param user_email: User email.
        :type user_email: str
        :param user_pwd: User password.
        :type user_pwd: str
        :return: User instance.
        :rtype: User
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = self.search_users({'email': user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> 'User':
        """
        Retrieves the User instance for a request.

        :param request: The Flask request object.
        :type request: Request
        :return: The User instance.
        :rtype: User
        """
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None

        base64_auth_header = self.extract_base64_authorization_header(
                authorization_header)
        if base64_auth_header is None:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(
                base64_auth_header)
        if decoded_auth_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
                decoded_auth_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
