# -*- coding: utf-8 -*-

"""Data Model"""
import base64
import binascii
import logging
import uuid
import os
from typing import ByteString

from config import Config
from crypto import Crypto
from database import Database
from datamodel import User
from errors import AppError
from singleton import Singleton

DEFAULT_USER = os.environ.get('USER')
DEFAULT_EMAIL = DEFAULT_USER + "@email.org"

logger = logging.getLogger(__name__)


class UserService(metaclass=Singleton):

    def __init__(self, db=None, config=Config):
        self._db = db or Database()
        self._config = config or Config()
        self._owner = None

    def get_owner(self) -> User:
        if not self._owner:
            self._owner = self._db.get(User, 1)
        return self._owner

    def set_owner(self, name: str = DEFAULT_USER, email: str = DEFAULT_EMAIL) -> User:
        if self._db.get(User, 1):
            AppError("User 1 already registered")
            return None
        uid = str(uuid.uuid4())
        crypto = Crypto(self.config.rsabits)
        self._owner = User(uid=str(uuid.uuid4()), name=name, email=email, pubkey=crypto.pubkey, privkey=crypto.privkey)
        return self.db.add(self._owner)

    def register(self, uid: str, name: str, email: str, pubstr: str) -> User:
        try:
            pubkey = base64.b64decode(pubstr)
        except binascii.Error as e:
            AppError(e)
            return None
        user = User(uid=uid, name=name, email=email, pubkey=pubkey)
        return self._db.add(user)
