# -*- coding: utf-8 -*-

"""Data Model"""
import base64
import binascii
import logging
import uuid
import os
from typing import List, Union

from config import Config
from crypto import Crypto
from database import Database
from datamodel import User
from status import Status
from singleton import Singleton

DEFAULT_USER = os.environ.get('USER')
DEFAULT_EMAIL = DEFAULT_USER + "@email.org"

logger = logging.getLogger(__name__)


class UserService(metaclass=Singleton):

    def __init__(self, db=None, config=None):
        self._db = db or Database()
        self._config = config or Config()
        self._owner = None

    def registered(self) -> User:
        if not self._owner:
            self._owner = self._db.get(User, 1)
        return self._owner

    def register(self, name: str = DEFAULT_USER, email: str = DEFAULT_EMAIL) -> Union[User, None]:
        if self._db.get(User, User.sid == 1):
            Status.failed("Owner is already registered", logger)
            return None
        uid = str(uuid.uuid4())
        crypto = Crypto(self._config.rsabits, genkeys=True)
        self._owner = User(uid=uid, name=name, email=email, pubkey=crypto.pubkey, privkey=crypto.privkey)
        return self._db.add(self._owner)

    def add(self, uid: str, name: str, email: str, pubstr: str) -> Union[User, None]:
        try:
            pubkey = base64.b64decode(pubstr)
        except binascii.Error as e:
            Status.catched(e, logger)
            return None
        user = User(uid=uid, name=name, email=email, pubkey=pubkey)
        return self._db.add(user)

    def list(self) -> List[User]:
        return self._db.list(User)