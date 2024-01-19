#!/usr/bin/env python3
"""
User views module.
"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User
from api.v1.auth import Auth


@app_views.route('/users/me', methods=['GET'], strict_slashes=False)
def get_me() -> str:
    """
    Retrieves the authenticated User object.
    """
    user = Auth().current_user(request)
    if not user:
        abort(404)

    return jsonify(user.to_json()), 200
