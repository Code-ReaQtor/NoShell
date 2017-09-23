#!/usr/bin/env python
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez."
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"

socketio = SocketIO(engineio_logger=True)
token_cache = SimpleCache()  # FIXME: Needs a TTL Cache with callback to disconnect socketIO clients.
login_manager = LoginManager()
database = SQLAlchemy()
