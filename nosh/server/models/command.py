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


class Command(Base):
    __tablename__ = 'command'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    format = Column(String(50), nullable=False)

    def __repr__(self):
        return "<Command {}>".format(self.name)
