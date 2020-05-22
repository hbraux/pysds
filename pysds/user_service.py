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

    def __init__(self):
        self.config = Config()
        self.database = Database()
        self.admin = self.database.get(User, User.sid == 1)

    def create_admin(self):
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
        self.admin = admin

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

    @staticmethod
    def init():
        try:
            Config.create()
            Database.create()
        except Exception as e:
            return Service().catched(e)
        service = UserService()
        service.create_admin()
        return service


