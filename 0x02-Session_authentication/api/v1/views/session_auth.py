#!/usr/bin/env python3
"""Module for session authenticating views.
"""


from flask import jsonify, request
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """
    POST /api/v1/auth_session/login
    Handles user login via session authentication.
    """
    # Retrieve email and password from POST request
    email = request.form.get('email')
    password = request.form.get('password')

    # Case 1: Missing email
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Case 2: Missing password
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Case 3: Find user by email
    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]  # Use the first matched user

    # Case 4: Check if password is valid
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Case 5: Successful login, create session
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)
    return response`
