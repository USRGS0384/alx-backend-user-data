#!/usr/bin/env python3
"""
Basic Flask app for a minimal WSGI application
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome() -> str:
    """
    Index route that returns a json paylod
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    Registers a user using AUTH
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    Creates a new session for a user on valid information
    stores in a cookie and returns it as a header
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """
    Gets request from request cookies finds user associated
    with session_id if existing destroy's the session, redirects
    to index and if doesn't exist raise a 403 error
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('/'))
    abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """
    Finds user if existing in session or abort
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
