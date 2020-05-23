# -*- coding: utf-8 -*-

"""Data Model"""
import json
import logging
import os
import uuid
from typing import Union

from pysds.crypto import Crypto
from pysds.database import Database
from pysds.datamodel import *
from pysds.service import Service
from pysds.user_service import UserService

logger = logging.getLogger(__name__)


class DatasetService(Service):
    UUID = uuid.UUID("5ab43121-a28c-4a38-8e9a-f5904f20ec05")
    VERSION = 1  # max 255
    EXTENSION = '.sds'
    NAME_LEN = 128

    def __init__(self):
        self._database = Database()
        self._user_service = UserService()

    def imp(self, name: str, infile: str, metadata: dict, outfile=None, ignore=False) -> Union[Dataset, None]:
        if self._database.get(Dataset, Dataset.name == name):
            return self.failed(f"a dataset with name {name} is already in local store")
        if not outfile:
            outfile = os.path.abspath(os.path.splitext(infile)[0] + self.EXTENSION)
        if not ignore and os.path.isfile(outfile):
            return self.failed(f"file {outfile} already exists")
        admin = self._user_service.admin()
        dsid = uuid.uuid4()
        crypto = Crypto(admin.pubkey, admin.privkey, secret=dsid.bytes)
        with open(outfile, "wb") as out:
            out.write(self.UUID.bytes)
            out.write(bytes([self.VERSION]))
            out.write(dsid.bytes)
            out.write(uuid.UUID(admin.uid).bytes)
            out.write(name.ljust(self.NAME_LEN, ' ').encode()[:self.NAME_LEN])
            crypto.write(out, json.dumps(metadata))
            with open(infile, "r") as inp:
                for line in inp:
                    crypto.write(out, line)
            logger.info(f"file {outfile} created")
        ds = Dataset(uid=str(dsid), name=name, owner=Dataset.OWNED, file=outfile)
        try:
            self._database.add(ds)
        except Exception as e:
            return self.catched(e)
        return ds

    def load(self, datafile) -> Union[Dataset, None]:
        with open(datafile, "rb") as rio:
            if rio.read(16) != self.UUID.bytes:
                return self.failed(f"{datafile} is not a DataSet file")
            version = rio.read(1)[0]
            if version != self.VERSION:
                return self.failed(f"File version {version} not supported")
            dsid = str(uuid.UUID(bytes=rio.read(16)))
            owner = str(uuid.UUID(bytes=rio.read(16)))
            name = rio.read(self.NAME_LEN).decode().rstrip()
        if self._database.get(Dataset, Dataset.uid == dsid):
            return self.failed(f"Dataset {dsid} already in local store")
        if not self._database.get(User, User.uid == owner):
            return self.failed(f"User {owner} is unknown (must be registered)")
        ds = Dataset(uid=str(dsid), name=name, owner=owner, file=datafile)
        try:
            self._database.add(ds)
        except Exception as e:
            return self.catched(e)
        return ds

