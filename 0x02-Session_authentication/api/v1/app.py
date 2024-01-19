#!/usr/bin/env python3
"""
Main application file for Holberton School's backend project.
"""


import os
from api.v1.app import app
from api.v1.auth import Auth, BasicAuth, SessionAuth
from api.v1.views.index import app_views
from flask import request, abort


class AuthSelector:
    """
    AuthSelector class to manage authentication types.
    """
    def __init__(self):
        """
        Initializes AuthSelector with basic and session
        authentication instances.
        """
        self.auth_basic = BasicAuth()
        self.auth_session = SessionAuth()

    def select_auth(self) -> Auth:
        """
        Selects the appropriate authentication type
        based on the environment variable AUTH_TYPE.
        Returns:
            Auth: Selected authentication instance.
        """
        if os.getenv('AUTH_TYPE') == 'session_auth':
            return self.auth_session
        return self.auth_basic


auth_selector = AuthSelector()
auth = auth_selector.select_auth()
app.before_request(auth.require_auth)

app.register_blueprint(app_views)


@app.before_request
def before_request():
    """
    Before request method for additional authentication checks.
    """
    excluded_paths = ['/api/v1/auth_session/login/']
    if request.path not in excluded_paths and not auth.authorization_header(
            request) and not auth.session_cookie(request):
        abort(401)
