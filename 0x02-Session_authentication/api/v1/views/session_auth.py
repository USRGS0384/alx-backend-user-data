#!/usr/bin/env python3
"""View for session authentication
"""


from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from os import getenv
import uuid


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """Handles user login through session authentication."""
    return jsonify({"message": "Login route"}), 200
    # Validate email
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Validate password
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Find user by email
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    # Validate password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create session ID
    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    # Set cookie
    response = jsonify(user.to_dict())
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response
