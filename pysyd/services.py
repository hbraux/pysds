# -*- coding: utf-8 -*-

"""Data Model"""
import base64
import binascii
import json
import uuid
import os
import logging
from typing import List, Union

from injector import inject, Injector

from pysyd.config import Config
from pysyd.crypto import Crypto
from pysyd.database import Database
from pysyd.datamodel import User, Dataset

logger = logging.getLogger(__name__)


class Service:
    _error_msg = None

    @classmethod
    def failed(cls, msg, *args, **kwargs) -> None:
        logger.error(msg, *args, **kwargs)
        # TODO: format args
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
        self.admin = self.create_admin() if config.setup else self.database.get(User, User.sid == 1)

    def create_admin(self) -> Union[User, None]:
        uuid4 = uuid.uuid4()
        crypto = Crypto()
        crypto.genkeys(self.config.keylen)
        username = os.environ.get('USER')
        email = username + "@admin"
        admin = User(uid=str(uuid4), name=username, email=email, pubkey=crypto.pubkey, privkey=crypto.privkey)
        try:
            self.database.add(admin)
        except Exception as e:
            return self.catched(e)
        logger.info("Admin user created")
        return admin

    def add(self, uid: uuid.UUID, name: str, email: str, pubstr: str) -> Union[User, None]:
        try:
            pubkey = base64.b64decode(pubstr)
        except binascii.Error as e:
            return self.catched(e)
        user = User(uid=str(uid), name=name, email=email, pubkey=pubkey)
        try:
            self.database.add(user)
        except Exception as e:
            return self.catched(e)
        return user

    def list(self) -> List[User]:
        return self.database.list(User)


class DatasetService(Service):
    DATASET_UUID = "5ab43121-a28c-4a38-8e9a-f5904f20ec05"
    DATASET_VERSION = 1
    DATASET_EXTENSION = '.syd'

    @inject
    def __init__(self, database: Database, config: Config, us: UserService):
        self.database = database
        self.config = config
        self.admin: User = us.admin

    def add(self, name: str, infile: str, meta: dict, outfile=None, ignore=False) -> Union[Dataset, None]:
        if self.database.get(Dataset, Dataset.name == name):
            return self.failed("a dataset with name %s is already in the store")
        if not outfile:
            outfile = os.path.abspath(os.path.splitext(infile)[0] + self.DATASET_EXTENSION)
        if not ignore and os.path.isfile(outfile):
            return self.failed("file %s already exists", outfile)
        uuid4 = uuid.uuid4()
        crypto = Crypto(self.admin.pubkey, self.admin.privkey, secret=uuid4.bytes)
        with open(outfile, "wb") as out:
            out.write(uuid.UUID(self.DATASET_UUID).bytes)
            out.write(self.DATASET_VERSION.to_bytes(2, 'little'))
            out.write(uuid4.bytes)
            out.write(uuid.UUID(self.admin.uid).bytes)
            crypto.write(out, json.dumps(meta))
            with open(infile, "r") as inp:
                for line in inp:
                    crypto.write(out, line)
            logger.info("file %s created", outfile)
        ds = Dataset(uid=str(uuid4), name=name, meta="", owner=self.admin.uid, file=outfile)
        try:
            self.database.add(ds)
        except Exception as e:
            return self.catched(e)
        return ds

    def add_external(self, reader) -> Dataset:
        raise NotImplementedError()


class Token(Service):
    TOKEN_UUID = "a6416f6a-eb43-4494-ab49-61c148e61d9c"
    TOKEN_VERSION = 1

    def __init__(self, database: Database):
        self.database = database


class Services(Service):
    _injector = Injector()
    _us = None
    _ds = None

    @classmethod
    def init(cls):
        cls._injector.binder.bind(Config, to=Config(setup=True))
        try:
            cls._us = cls._injector.get(UserService)
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
            cls._ds = cls._injector.get(Dataset)
        return cls._ds
