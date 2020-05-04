# -*- coding: utf-8 -*-

"""Data Model"""
import base64
import binascii
import uuid
import os
import logging
from typing import List, Union

from injector import inject

from config import Config
from crypto import Crypto
from database import Database
from datamodel import User
from status import Status

logger = logging.getLogger(__name__)


class UserService:

    @inject
    def __init__(self, database: Database, config: Config):
        self.database = database
        self.config = config
        self.admin = self.database.get(User, User.sid == 1) or self.create_admin()

    def create_admin(self) -> User:
        uid = str(uuid.uuid4())
        crypto = Crypto(self.config.rsabits, genkeys=True)
        username = os.environ.get('USER')
        email = username + "@admin"
        self.admin = User(uid=uid, name=username, email=email, pubkey=crypto.pubkey, privkey=crypto.privkey)
        return self.database.add(self.admin)

    def add(self, uid: str, name: str, email: str, pubstr: str) -> Union[User, None]:
        try:
            pubkey = base64.b64decode(pubstr)
        except binascii.Error as e:
            logger.error(e)
            Status.catched(e)
            return None
        user = User(uid=uid, name=name, email=email, pubkey=pubkey)
        return self.database.add(user)

    def list(self) -> List[User]:
        return self.database.list(User)
