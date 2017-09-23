#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey

from nosh.server.models import Base


__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez."
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"


class Credential(Base):
    __tablename__ = 'credential'

    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(String, nullable=False)
    username = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    command_id = Column(Integer, ForeignKey('command.id'))

    def __repr__(self):
        return "<Credential {}>".format(self.host)
