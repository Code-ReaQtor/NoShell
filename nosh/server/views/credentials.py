#!/usr/bin/env python
import json

import binascii
import flask_socketio
from flask import render_template, url_for, session, request
from flask.views import MethodView
from flask_login import current_user
from werkzeug.utils import redirect

from nosh.server import database
from nosh.server.models.command import Command
from nosh.server.models.credential import Credential
from nosh.server.views import decrypt

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
        return render_template('credentials.html', credentials=credentials, hexlify=binascii.hexlify)

    def post(self):
        credential_id = json.loads(request.data)
        credential = database.session.query(Credential).filter_by(id=credential_id).first()
        command = database.session.query(Command).filter_by(id=credential.command_id).first()
        if credential and command:
            command_ = command.format.format(username=credential.username, host=credential.host)
            flask_socketio.emit('execute', {'command': command_, 'password': decrypt(credential.password)},
                                namespace='/auth', room=session['room'])
        return redirect(url_for('credentials'))
