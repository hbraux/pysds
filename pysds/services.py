# -*- coding: utf-8 -*-

"""Data Model"""
import base64
import binascii
import uuid
import os
import logging
from typing import List, Union

from injector import inject, Injector

from pysds.config import Config
from pysds.crypto import Crypto
from pysds.database import Database
from pysds.datamodel import User

logger = logging.getLogger(__name__)

class Service:
    _error_msg = None

    @classmethod
    def failed(cls, msg: str) -> None:
        logger.error(msg)
        cls._error_msg = msg
        return None

    @classmethod
    def catched(cls, e: Exception) -> None:
        msg = type(e).__name__ + ': ' + getattr(e, 'message', str(e)).partition('\n')[0]
        return cls.failed(msg)

    @classmethod
    def failure(cls) -> bool:
        return cls._error_msg is not None

    @classmethod
    def success(cls) -> bool:
        return cls._error_msg is None


    @classmethod
    def errormsg(cls) -> str:
        return cls._error_msg


class UserService(Service):

    @inject
    def __init__(self, database: Database, config: Config):
        self.database = database
        self.config = config
        self.admin = None

    def create_admin(self) -> Union[User, None]:
        uid = str(uuid.uuid4())
        crypto = Crypto()
        crypto.genkeys(self.config.keylen)
        username = os.environ.get('USER')
        email = username + "@admin"
        self.admin = User(uid=uid, name=username, email=email, pubkey=crypto.pubkey, privkey=crypto.privkey)
        try:
            self.database.add(self.admin)
        except Exception as e:
            return self.catched(e)
        logger.info("Admin user created")
        return self.admin

    def add(self, uid: str, name: str, email: str, pubstr: str) -> Union[User, None]:
        try:
            pubkey = base64.b64decode(pubstr)
        except binascii.Error as e:
            return self.catched(e)
        user = User(uid=uid, name=name, email=email, pubkey=pubkey)
        try:
            self.database.add(user)
        except Exception as e:
            return self.catched(e)
        return user

    def list(self) -> List[User]:
        return self.database.list(User)


class DatasetService(Service):

    @inject
    def __init__(self, database: Database, config: Config):
        self.database = database
        self.config = config


class Services(Service):
    _injector = Injector()
    _us = None
    _ds = None

    @classmethod
    def init(cls):
        cls._injector.binder.bind(Config, to=Config(setup=True))
        try:
            cls._us = cls._injector.get(UserService)
            return cls._us.create_admin()
        except Exception as e:
            return cls.catched(e)

    @classmethod
    def user(cls) -> UserService:
        if not cls._us:
            cls._us = cls._injector.get(UserService)
        return cls._us

    @classmethod
    def dataset(cls) -> DatasetService:
        if not cls._ds:
            cls._us = cls._injector.get(UserService)
        return cls._ds