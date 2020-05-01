# -*- coding: utf-8 -*-

"""Application core"""

import os
import logging
import uuid
import io
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pysds.crypto import Crypto
from pysds.model import User

logger = logging.getLogger(__name__)

class App(object):

    @staticmethod
    def get_instance(cfgpath):
        if os.path.isdir(cfgpath):
            with open(cfgpath + "/dburl") as file:
                dburl = file.read()
        return App(dburl)

    @staticmethod
    def init(cfgpath, dburl, bits, username, email):
        logger.info("Creating dir %s", cfgpath)
        os.makedirs(cfgpath)
        crypto = Crypto(bits=bits)
        app = App(dburl)
        app.register(str(uuid.uuid4()), username, email, crypto.pubkey, crypto.privkey)
        return App

    def __init__(self, dburl: str):
        engine = create_engine(dburl)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.owner = self.session.query(User).filter(id == 1)
        if not self.owner:
            err = "unable to find default user in database"
            logging.error(err)
            raise Exception(err)
        logger.info("User registered %s", self.owner)

    def register(self, uuid: str, username: str, email: str, pubkey: str, privkey: str = None):
        user = User(uuid=uuid, username=username, email=email, pubkey=pubkey, privkey=privkey)
        self.session.add(user)
        self.session.commit()
