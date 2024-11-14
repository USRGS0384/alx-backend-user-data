#!/usr/bin/env python3
"""
SessionAuth
"""

from flask import Blueprint, jsonify, request, make_response
from models.user import User  # Assuming you have a User model
from api.v1.auth.session_auth import SessionAuth  # Assuming SessionAuth handles session creation

auth_session = Blueprint('auth_session', __name__)
session_auth = SessionAuth()  # Instantiate the session authentication handler

@auth_session.route('/api/v1/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Login route that creates a session for a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve user by email
    user = User.search({"email": email})
    if not user or not user[0].is_valid_password(password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    user = user[0]
    
    # Create session ID
    session_id = session_auth.create_session(user.id)
    if not session_id:
        return jsonify({"error": "Internal server error"}), 500
    
    # Set session ID in a cookie
    response = jsonify(user.to_dict())
    response.set_cookie("_my_session_id", session_id)
    return response, 200

@auth_session.route('/api/v1/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout route that destroys the user session"""
    session_id = request.cookies.get('_my_session_id')
    if not session_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Destroy the session
    if not session_auth.destroy_session(session_id):
        return jsonify({"error": "Unauthorized"}), 401

    response = jsonify({"message": "Successfully logged out"})
    response.delete_cookie('_my_session_id')  # Remove session cookie
    return response, 200
