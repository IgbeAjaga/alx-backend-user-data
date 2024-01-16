#!/usr/bin/env python3
"""
Main module of the API
"""


from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from os import getenv
from api.v1.auth.auth import Auth


app = Flask(__name__)
app.register_blueprint(app_views)

CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

auth = None
auth_type = getenv("AUTH_TYPE")

if auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
else:
    auth = Auth()


@app.before_request
def before_request():
    """
    Before request handler.
    """
    if auth is None:
        return
    excluded_paths = [
            '/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", default="0.0.0.0")
    port = getenv("API_PORT", default=5000)
    app.run(host=host, port=port, threaded=True)
