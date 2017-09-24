#!/usr/bin/env python
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pexpect
import webview
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from nosh.server import application, socketio
from socketIO_client import SocketIO, BaseNamespace

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez."
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"


import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


HOST = 'localhost'
PORT = 8080
socketio_client = None

commands = []


class ClientNamespace(BaseNamespace):

    def on_get_token(self, *args):
        token = args[0]['token']
        sid = args[0]['sid']
        login_url = "http://{}:{}/login?token={}&sid={}".format(HOST, PORT, token, sid)
        print(login_url)
        webview.load_url(login_url)

    def on_execute(self, *args):
        global commands
        commands += args
        socketio_client.disconnect()
        socketio.stop()
        webview.destroy_window()


def setup_database():
    from nosh.server.models import Base
    from nosh.server.models.command import Command
    from nosh.server.models.credential import Credential
    from nosh.server.models.user import User

    engine = create_engine(application.config['SQLALCHEMY_DATABASE_URI'])
    if not engine.dialect.has_table(engine, 'user'):
        Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)
    setup_default_commands(session)


def setup_default_commands(session):
    from nosh.server.models.command import Command
    command = Command()
    command.name = 'Secure Shell(SSH)'
    command.format = 'ssh {username}@{host}'
    session.add(command)
    session.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Password manager and automation tool for SSH, SCP, etc.')
    parser.add_argument('-p', '--port', type=int, default=8080, help='port for nosh HTTP server')
    args = parser.parse_args()
    PORT = args.port

    home = Path.home()
    config = home / '.nosh'
    if not config.exists():
        config.mkdir()
        setup_database()

    with ThreadPoolExecutor() as executor:
        # run server
        result = executor.submit(socketio.run, application, host='localhost', port=PORT)

        # run socketIO client
        socketio_client = SocketIO('localhost', PORT)
        auth_namespace = socketio_client.define(ClientNamespace, '/auth')
        auth_namespace.emit('get_token')
        executor.submit(socketio_client.wait)

        # create_window() should be on the main thread
        webview.create_window('NoShell', "http://{}:{}/".format(HOST, PORT))

    # execute process here
    for command in commands:
        print(command)
        child = pexpect.spawn(command['command'])
        child.expect('Password')  # FIXME: not always the exact word
        child.interact()
        break  # TODO: jump server
