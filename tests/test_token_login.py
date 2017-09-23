#!/usr/bin/env python
import secrets
import unittest

from bs4 import BeautifulSoup

from nosh.server import application, socketio

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez"
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"


class TokenLoginTest(unittest.TestCase):

    def setUp(self):
        self.flask_client = application.test_client(self)
        self.socketio_client = socketio.test_client(application, namespace='/auth')
        self.assertListEqual([], self.socketio_client.get_received('/auth'))

    def get_credentials(self):
        self.socketio_client.emit('get_token', namespace='/auth')
        response = self.socketio_client.get_received('/auth')
        data = response[0]['args'][0]
        return data['token'], data['sid']

    def test_auth_should_return_token(self):
        self.get_credentials()

    def test_invalid_token_should_return_error_page(self):
        token = secrets.token_urlsafe(50)
        response = self.flask_client.get('/login', query_string={'token': token})
        self.assertEqual(400, response.status_code)
        self.assertEqual(b'Invalid token!', response.data)
        response = self.socketio_client.get_received('/auth')
        self.assertEqual(0, len(response))

    def test_valid_token_should_continue_to_login_page(self):
        token, sid = self.get_credentials()
        response = self.flask_client.get('/login', query_string={'token': token, 'sid': sid})
        self.assertEqual(200, response.status_code)
        html_parser = BeautifulSoup(response.data, 'html.parser')
        form = html_parser.find('form')
        self.assertIsNotNone(form)
        self.assertIsNotNone(form.find(attrs={'name': 'user_id'}))
        self.assertIsNotNone(form.find(attrs={'name': 'password'}))
        response = self.socketio_client.get_received('/auth')
        self.assertEqual('authenticated!', response[0]['args']['message'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
