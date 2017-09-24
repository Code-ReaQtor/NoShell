#!/usr/bin/env python

import os
from pathlib import Path

from flask import Flask
from flask_login import login_required

from nosh.server.models.user import User
from nosh.server.namespaces.token import TokenNamespace
from nosh.server.plugins import socketio, login_manager, database
from nosh.server.views.credentials import Credentials
from nosh.server.views.add_credential import AddCredential
from nosh.server.views.login import Login
from nosh.server.views.register import Register

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez."
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')

application = Flask(__name__)

application.config['SECRET_KEY'] = os.urandom(50)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/.nosh/nosh.db'.format(Path.home())
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio.init_app(application)
database.init_app(application)

login_manager.init_app(application)
login_manager.login_view = 'login'

# application.logger.setLevel(logging.DEBUG)


@login_manager.user_loader
def load_user(user_id) -> User:
    return database.session.query(User).get(int(user_id))


socketio.on_namespace(TokenNamespace('/auth'))

application.add_url_rule('/login', view_func=Login.as_view('login'))
application.add_url_rule('/register', view_func=Register.as_view('register'))
application.add_url_rule('/credentials', view_func=login_required(Credentials.as_view('credentials')))
application.add_url_rule('/add-credential', view_func=login_required(AddCredential.as_view('add-credential')))
