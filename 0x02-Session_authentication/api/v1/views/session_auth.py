#!/usr/bin/env python3
"""View for session authentication
"""


from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """
    POST /api/v1/auth_session/login
    Handles user login through session authentication.
    """
    # Get email and password from the POST request
    email = request.form.get('email')
    password = request.form.get('password')

    # Case 1: Email is missing
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Case 2: Password is missing
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Case 3: Search for user by email
    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    # Get the first user found
    user = users[0]

    # Case 4: Incorrect password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Case 5: Correct email and password, create session ID
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())

    # Add session ID as a cookie
    session_name = getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
