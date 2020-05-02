# -*- coding: utf-8 -*-

"""Data Model"""
import base64
import binascii
import logging
from typing import ByteString

from database import Database
from datamodel import User
from errors import application_error
from singleton import Singleton

logger = logging.getLogger(__name__)


class UserService(metaclass=Singleton):

    def __init__(self, db=None):
        self.db = db or Database()

    def add(self, uid: str, name: str, email: str, pubkey: ByteString, privkey: ByteString = None) -> bool:
        pubbytes = pubkey
        if type(pubkey) is str:
            logger.debug("converted public key from Bytes64 string to bytes")
            try:
                pubbytes = base64.b64decode(pubkey)
            except binascii.Error as e:
                return application_error(e)
        user = User(uid=uid, name=name, email=email, pubkey=pubbytes, privkey=privkey)
        return self.db.add(user)


