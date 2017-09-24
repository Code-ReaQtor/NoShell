#!/usr/bin/env python
import hashlib

import bcrypt
import flask_socketio
from flask import request, render_template, session, url_for
from flask.views import MethodView
from flask_login import login_user
from sqlalchemy.sql.functions import count
from werkzeug.utils import redirect

from nosh.server.models.user import User
from nosh.server.plugins import token_cache, database
from nosh.server.views import VALID_CHARACTERS

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez."
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"


def is_valid_user():
    if session.get('valid_user', False):
        return True
    token = request.args.get('token', None)
    sid = request.args.get('sid', None)
    if token and sid:
        room = token_cache.get(token)
        if room == sid:
            session['room'] = room
            return True
    return False


class Login(MethodView):

    def get(self):
        if is_valid_user():
            session['valid_user'] = True
            user_count = database.session.query(count(User.id)).scalar()
            if user_count:
                flask_socketio.send({'message': 'authenticated!'}, namespace='/auth', room=session['room'])
                users = [user for user in database.session.query(User)]
                return render_template('login.html', users=users)
            else:
                return render_template('register.html')
        return "Invalid token!", 400

    def post(self):
        user_id = request.form.get('user_id', None)
        password = request.form.get('password', None)

        if not user_id.isdigit() or not password or not all(map(lambda x: x in VALID_CHARACTERS, password)):
            return redirect(url_for('login'))

        user = database.session.query(User).filter_by(id=user_id).first()
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return redirect(url_for('login'))

        password_hash = hashlib.sha256(password.encode('utf-8')).digest()
        session['password_hash'] = password_hash  # will be used for encrypting/decrypting credential passwords
        login_user(user)
        return redirect(url_for('credentials'))
