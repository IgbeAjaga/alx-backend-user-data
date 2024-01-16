#!/usr/bin/env python3
""" Main application module
"""

from flask import Flask, jsonify, abort, request
from api.v1.views.index import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
app.register_blueprint(app_views)

auth_type = app.config.get('AUTH_TYPE')
auth = BasicAuth() if auth_type == 'basic_auth' else Auth()

@app.before_request
def before_request():
    """ Before request handler
    """
    if auth is None or not auth.require_auth(request.path, [
            '/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
