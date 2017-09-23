#!/usr/bin/env python
import unittest

from nosh.server import application

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez"
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"


class CredentialsPageTest(unittest.TestCase):

    def setUp(self):
        self.flask_client = application.test_client(self)

    def test_no_login(self):
        response = self.flask_client.get('/credentials')
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://localhost/login?next=%2Fcredentials', response.headers['Location'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
