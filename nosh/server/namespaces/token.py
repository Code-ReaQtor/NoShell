#!/usr/bin/env python
import secrets

from flask import request
from flask_socketio import Namespace, emit

from nosh.server.plugins import token_cache

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez."
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"


class TokenNamespace(Namespace):

    def on_get_token(self):
        token = secrets.token_urlsafe(50)
        """
        https://flask-socketio.readthedocs.io/en/latest/#rooms
        All clients are assigned a room when they connect, named with the session ID of the connection, which can be 
        obtained from request.sid.
        """
        token_cache.set(token, request.sid)
        emit('get_token', {'token': token, 'sid': request.sid}, namespace='/auth')
