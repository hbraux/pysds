# -*- coding: utf-8 -*-

"""Data Model"""
import logging
import uuid
from typing import Union

from injector import inject

from pysds.database import Database
from pysds.datamodel import *
from pysds.service import Service
from pysds.user_service import UserService

logger = logging.getLogger(__name__)


class TokenService(Service):
    TOKEN_UUID = "a6416f6a-eb43-4494-ab49-61c148e61d9c"
    TOKEN_VERSION = 1

    @inject
    def __init__(self):
        self.database = Database()
        self.admin = UserService().admin

    def create(self, uid: uuid.UUID = None, sid: int = None) -> Union[Dataset, None]:
        ds = self.database.get(Dataset, Dataset.uid == uid) if uid else self.database.get(Dataset, Dataset.sid == sid)
        if not ds:
            return self.failed(f"DataSet {uid or sid} is unknown")
        if ds.is_owned():
            return self.failed(f"DataSet {uid or sid} is owned")
        token = Token(uid=str(uuid.uuid4()), name=f"DataSet {ds.name}", dataset=ds.uid,
                      requester=self.admin.uid, granter=ds.owner)
        try:
            self.database.add(token)
        except Exception as e:
            return self.catched(e)
        return token
