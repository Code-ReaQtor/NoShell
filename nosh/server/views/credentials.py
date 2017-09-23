#!/usr/bin/env python
import json

import flask_socketio
from flask import render_template, url_for, session, request
from flask.views import MethodView
from flask_login import current_user
from sqlalchemy import exists
from werkzeug.utils import redirect

from nosh.server import database
from nosh.server.models.command import Command
from nosh.server.models.credential import Credential

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez."
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"


class Credentials(MethodView):

    def get(self):
        credentials = database.session.query(Credential).filter_by(user_id=current_user.id).all()
        return render_template('credentials.html', credentials=credentials)

    def post(self):
        credential_id = json.loads(request.data)
        credential = database.session.query(Credential).filter_by(id=credential_id).first()
        command = database.session.query(Command).filter_by(id=credential.command_id).first()
        if credential and command:
            command_ = command.format.format(credential.username, credential.host)
            flask_socketio.emit('execute', {'command': command_, 'password': credential.password},
                                namespace='/auth', room=session['room'])
        return redirect(url_for('credentials'))


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
        credential.password = password
        credential.user_id = current_user.id
        credential.command_id = command_id

        database.session.add(credential)
        database.session.commit()

        return redirect(url_for('credentials'))
