#!/usr/bin/env python
from flask import render_template, request, url_for
from flask.views import MethodView
from flask_login import current_user
from sqlalchemy import exists
from werkzeug.utils import redirect

from nosh.server import database
from nosh.server.models.command import Command
from nosh.server.models.credential import Credential
from nosh.server.views import encrypt

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez."
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"


class AddCredential(MethodView):
    def get(self):
        commands = database.session.query(Command).all()
        return render_template('add-credential.html', commands=commands)

    def post(self):
        command_id = request.form.get('command_id', None)
        host = request.form.get('host', None)
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        if not command_id or not host or not username or not password \
                or not database.session.query(exists().where(Command.id == command_id)).scalar():
            return redirect(url_for('add-credential'))

        credential = Credential()
        credential.host = host
        credential.username = username
        credential.password = encrypt(password)
        credential.user_id = current_user.id
        credential.command_id = command_id

        database.session.add(credential)
        database.session.commit()

        return redirect(url_for('credentials'))
