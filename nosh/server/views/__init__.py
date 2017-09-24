#!/usr/bin/env python
import io
import string

from flask import session
from twofish import Twofish

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez."
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"

VALID_CHARACTERS = string.ascii_letters + string.digits + string.punctuation


def yield_chunks(data: bytes, size: int) -> bytes:
    with io.BytesIO(data) as f:
        while True:
            chunk = f.read(size)
            i = len(chunk)
            if i == 0:
                raise StopIteration
            if i < size:
                chunk += b'\0' * (size - i)
            yield chunk


def encrypt(password: str) -> bytes:
    twofish = Twofish(session['password_hash'])
    encrypted = b''
    for chunk in yield_chunks(password.encode('utf-8'), 16):
        encrypted += twofish.encrypt(chunk)
    return encrypted


def decrypt(password: bytes) -> str:
    twofish = Twofish(session['password_hash'])
    decrypted = b''
    for chunk in yield_chunks(password, 16):
        decrypted += twofish.decrypt(chunk)
    return decrypted.rstrip(b'\0').decode('utf-8')


