#!/usr/bin/env python
from sqlalchemy import Column, Integer, String

from nosh.server.models import Base

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez."
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return "<User {}>".format(self.name)
