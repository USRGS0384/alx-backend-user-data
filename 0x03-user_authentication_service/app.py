#!/usr/bin/env python3
"""
Basic flask application for User Authentication Service
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect, make_response
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def get_message():
    """Get message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ Register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """Login user
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
    except KeyError:
        abort(400)

    try:
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response
        else:
            abort(401)
    except NoResultFound:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Logout the user and destroy their session."""
    session_id = request.cookies.get('session_id')
    if not session_id:
        app.logger.debug("No session_id in cookies")
        abort(403)  # Forbidden

    # Find the session in the database
    session = Session.find_by_session_id(session_id)
    app.logger.debug(f"Session ID: {session_id}, Session: {session}")

    if session is None:
        app.logger.debug("Session not found")
        abort(403)  # Forbidden

    try:
        # Delete the session
        session.delete()
        app.logger.debug("Session deleted successfully")
    except Exception as e:
        app.logger.error(f"Error deleting session: {e}")
        abort(500)  # Internal Server Error

    # Prepare the response with a redirection to '/'
    response = make_response(redirect('/'))
    response.delete_cookie('session_id')  # Clear the session_id cookie
    return response


@app.route('/profile', strict_slashes=False)
def profile():
    """ Get user profile
    """
    session_id = request.cookies.get('session_id', None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ Get reset password token
    """
    try:
        email = request.form.get('email')
    except KeyError:
        abort(400)

    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    else:
        return jsonify({"email": email, "reset_token": token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ Update password end-point
    """
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
    except KeyError:
        abort(400)

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    else:
        return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
