# -*- coding: utf-8 -*-

"""Data Model"""
import base64
import binascii
import json
import logging
import os
import uuid
from typing import List, Union

from injector import inject, Injector

from pysds.config import Config
from pysds.crypto import Crypto
from pysds.database import Database
from pysds.datamodel import User, Dataset

logger = logging.getLogger(__name__)


class Service:
    _error_msg = None

    @classmethod
    def failed(cls, msg) -> None:
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
    def __init__(self, config: Config, database: Database):
        self.database = database
        self.config = config
        logger.debug(f"injected: {config} {database}")
        self.admin = self.create_admin() if config.setup else self.database.get(User, User.sid == 1)

    def create_admin(self) -> Union[User, None]:
        uuid4 = uuid.uuid4()
        crypto = Crypto()
        crypto.genkeys(self.config.keylen)
        username = os.environ.get('USER')
        admin = User(uid=str(uuid4), name=username, email="@admin", pubkey=crypto.pubkey, privkey=crypto.privkey)
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
    UUID = uuid.UUID("5ab43121-a28c-4a38-8e9a-f5904f20ec05")
    VERSION = 1 # max 255
    EXTENSION = '.sds'
    NAME_LEN = 128
    OWNED = 'owned'

    @inject
    def __init__(self, config: Config, userservice: UserService):
        logger.debug(f"injected: {config} {userservice}")
        self.config = config
        self.userservice = userservice
        # TODO: injecting db create duplicates
        self.database = userservice.database

    def add(self, name: str, infile: str, metadata: dict, outfile=None, ignore=False) -> Union[Dataset, None]:
        if self.database.get(Dataset, Dataset.name == name):
            return self.failed(f"a dataset with name %s is already in database")
        if not outfile:
            outfile = os.path.abspath(os.path.splitext(infile)[0] + self.EXTENSION)
        if not ignore and os.path.isfile(outfile):
            return self.failed(f"file {outfile} already exists")
        dsid = uuid.uuid4()
        crypto = Crypto(self.userservice.admin.pubkey, self.userservice.admin.privkey, secret=dsid.bytes)
        with open(outfile, "wb") as out:
            out.write(self.UUID.bytes)
            out.write(bytes([self.VERSION]))
            out.write(dsid.bytes)
            out.write(uuid.UUID(self.userservice.admin.uid).bytes)
            out.write(name.ljust(self.NAME_LEN, ' ').encode()[:self.NAME_LEN])
            crypto.write(out, json.dumps(metadata))
            with open(infile, "r") as inp:
                for line in inp:
                    crypto.write(out, line)
            logger.info(f"file {outfile} created")
        ds = Dataset(uid=str(dsid), name=name, owner=self.OWNED, file=outfile)
        try:
            self.database.add(ds)
        except Exception as e:
            return self.catched(e)
        return ds

    def add_external(self, datafile) -> Union[Dataset, None]:
        with open(datafile, "rb") as rio:
            if rio.read(16) != self.UUID.bytes:
                return self.failed(f"file {datafile} is not a Dataset")
            version = rio.read(1)[0]
            if version != self.VERSION:
                return self.failed(f"file version {version} not supported")
            dsid = str(uuid.UUID(bytes=rio.read(16)))
            owner = str(uuid.UUID(bytes=rio.read(16)))
            name = rio.read(self.NAME_LEN).decode().rstrip()
        if self.database.get(Dataset, Dataset.uid == dsid):
            return self.failed(f"Dataset {dsid} aready in database")
        if not self.database.get(User, User.uid == owner):
            return self.failed(f"User {owner} is unknown (must be registered)")
        ds = Dataset(uid=str(dsid), name=name, owner=owner, file=datafile)
        try:
            self.database.add(ds)
        except Exception as e:
            return self.catched(e)
        return ds


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
    def init(cls) -> Union[User, None]:
        cls._injector.binder.bind(Config, to=Config(setup=True))
        try:
            cls._us = cls._injector.get(UserService)
        except Exception as e:
            return cls.catched(e)
        return cls._us.admin

    @classmethod
    def user(cls) -> UserService:
        if not cls._us:
            cls._us = cls._injector.get(UserService)
        return cls._us

    @classmethod
    def dataset(cls) -> DatasetService:
        if not cls._ds:
            cls._ds = cls._injector.get(DatasetService)
        return cls._ds
