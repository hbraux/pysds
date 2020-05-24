# -*- coding: utf-8 -*-

"""Data Model"""
import logging
import uuid
from typing import Union

from pysds.database import Database
from pysds.datamodel import *
from pysds.dataset_service import DatasetService
from pysds.service import Service
from pysds.user_service import UserService

logger = logging.getLogger(__name__)


class TokenService(Service):
    TOKEN_UUID = "a6416f6a-eb43-4494-ab49-61c148e61d9c"
    TOKEN_VERSION = 1

    def __init__(self, database=Database, user_service=UserService, dataset_service=DatasetService):
        self.database = database()
        self.user_service = user_service()
        self.dataset_service = dataset_service()

    def create(self, uid: uuid.UUID = None, sid: int = None) -> Union[Dataset, None]:
        ds = self.dataset_service.find(uid)
        if not ds:
            return self.failed(f"DataSet {uid or sid} is unknown")
        if ds.is_owned():
            return self.failed(f"DataSet {uid or sid} is owned")
        admin = self.user_service.admin
        if not admin:
            return self.failed(self.user_service.errormsg())
        token = Token(uid=str(uuid.uuid4()), name=f"DataSet {ds.name}", dataset=ds.uid,
                      requester=admin.uid, granter=ds.owner)
        try:
            self.database.add(token)
        except Exception as e:
            return self.catched(e)
        return token
