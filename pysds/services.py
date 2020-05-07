# -*- coding: utf-8 -*-

"""Data Model"""
import base64
import binascii
import uuid
import os
import logging
from typing import List, Union

from injector import inject, Injector

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
        self.admin = None

    def create_admin(self) -> None:
        uid = str(uuid.uuid4())
        crypto = Crypto()
        crypto.genkeys(self.config.keylen)
        username = os.environ.get('USER')
        email = username + "@admin"
        self.admin = User(uid=uid, name=username, email=email, pubkey=crypto.pubkey, privkey=crypto.privkey)

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


class DataSetService:

    @inject
    def __init__(self, database: Database, config: Config):
        self.database = database
        self.config = config


class Services:
    injector = Injector()
    userService = injector.get(UserService)
    dataSetService = injector.get(DataSetService)

    @classmethod
    def init(cls):
        cls.userService.database.create()
        cls.userService.create_admin()

