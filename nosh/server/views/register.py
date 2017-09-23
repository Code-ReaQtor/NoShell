#!/usr/bin/env python
import bcrypt
from flask import render_template, url_for, request
from flask.views import MethodView
from werkzeug.utils import redirect

from nosh.server import database
from nosh.server.models.user import User
from nosh.server.views import VALID_CHARACTERS

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez."
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"


class Register(MethodView):

    def get(self):
        return render_template('register.html')

    def post(self):
        name = request.form.get('name', None)
        password = request.form.get('password', None)

        if not name or not password \
                or not all(map(lambda x: x in VALID_CHARACTERS + ' ', name)) \
                or not all(map(lambda x: x in VALID_CHARACTERS, password)):
            return redirect(url_for('register'))

        user = User()
        user.name = name
        user.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        database.session.add(user)
        database.session.commit()
        return redirect(url_for('login'))
