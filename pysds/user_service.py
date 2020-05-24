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
        self._config = Config()
        self._database = Database()
        self._admin = None

    def admin(self):
        if not self._admin:
            try:
                self._admin = self._database.get(User, User.is_admin is True)
            except Exception as e:
                return self.catched(e)
            if not self._admin:
                return self.failed("admin user is not created")
        return self._admin

    def add(self, uid: uuid.UUID, name: str, email: str, pubstr: str) -> Union[User, None]:
        try:
            pubkey = base64.b64decode(pubstr)
        except binascii.Error as e:
            return self.catched(e)
        user = User(uid=str(uid), name=name, email=email, pubkey=pubkey)
        try:
            self._database.add(user)
        except Exception as e:
            return self.catched(e)
        return user

    def list(self) -> List[User]:
        return self._database.list(User)

    def find(self, uid: uuid.UUID) -> Union[User, None]:
        try:
            return self._database.get(User, User.uid == str(uid))
        except Exception as e:
            return self.catched(e)

    def create(self) -> Union[User, None]:
        try:
            Config().create()
            Database().create()
        except Exception as e:
            return self.catched(e)
        return self.create_admin()

    def create_admin(self):
        uuid4 = uuid.uuid4()
        crypto = Crypto()
        crypto.genkeys(self._config.key_length)
        username = os.environ.get('USER')
        admin = User(uid=str(uuid4), name=username, email="@admin", is_admin=True, pubkey=crypto.pubkey, privkey=crypto.privkey)
        try:
            self._database.add(admin)
        except Exception as e:
            return self.catched(e)
        logger.info("Admin user created")
        self._admin = admin
        return admin

