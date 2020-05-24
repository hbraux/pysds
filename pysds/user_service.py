# -*- coding: utf-8 -*-
import binascii
import logging
import os
import uuid
from typing import List, Union

from pysds.config import Config
from pysds.crypto import Crypto
from pysds.database import Database
from pysds.datamodel import *
from pysds.service import Service

logger = logging.getLogger(__name__)


class UserService(Service):
    """Application Users Services"""""

    def __init__(self, config=Config, database=Database):
        self.config = config()
        self.database = database()
        self.admin = None
        try:
            self.admin = self.database.get(User, User.is_admin == 1)
        except Exception as e:
            self.catched(e)

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
        try:
            return self.database.list(User)
        except Exception as e:
            self.catched(e)
            return []

    def find(self, uid: uuid.UUID) -> Union[User, None]:
        try:
            return self.database.get(User, User.uid == str(uid))
        except Exception as e:
            return self.catched(e)

    @staticmethod
    def create():
        try:
            config = Config.create()
            Database.create(config.db_url)
        except Exception as e:
            return Service.catched(e)
        service = UserService()
        service.create_admin()
        return service

    def create_admin(self) -> Union[User, None]:
        uid = str(uuid.uuid4())
        crypto = Crypto()
        crypto.genkeys(self.config.key_length)
        username = os.environ.get('USER')
        admin = User(uid=uid, name=username, email="@admin", pubkey=crypto.pubkey, privkey=crypto.privkey, is_admin=True)
        try:
            self.database.add(admin)
        except Exception as e:
            return self.catched(e)
        logger.info("Admin user created")
        self.admin = admin
        return admin



