# -*- coding: utf-8 -*-

"""Data Model"""
import base64
import binascii
import uuid
import os
import logging
from typing import List, Union

from config import Config
from crypto import Crypto
from database import Database
from datamodel import User
from status import Status
from singleton import Singleton

logger = logging.getLogger(__name__)


class UserService(metaclass=Singleton):

    def __init__(self, db=None, config=None):
        self.db = db or Database()
        self.config = config or Config()
        self.admin = self.db.get(User, User.sid == 1) or self.create_admin()

    def create_admin(self) -> User:
        uid = str(uuid.uuid4())
        crypto = Crypto(self.config.rsabits, genkeys=True)
        username = os.environ.get('USER')
        email = username + "@admin"
        self.admin = User(uid=uid, name=username, email=email, pubkey=crypto.pubkey, privkey=crypto.privkey)
        return self.db.add(self.admin)

    def add(self, uid: str, name: str, email: str, pubstr: str) -> Union[User, None]:
        try:
            pubkey = base64.b64decode(pubstr)
        except binascii.Error as e:
            logger.error(e)
            Status.catched(e)
            return None
        user = User(uid=uid, name=name, email=email, pubkey=pubkey)
        return self.db.add(user)

    def list(self) -> List[User]:
        return self.db.list(User)
