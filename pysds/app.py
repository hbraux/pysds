# -*- coding: utf-8 -*-

"""Core Application"""

import os
import logging
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pysds.crypto import Crypto
from pysds.model import User

logger = logging.getLogger(__name__)


def get_app(cfgpath):
    if os.path.isdir(cfgpath):
        with open(cfgpath + "/dburl") as file:
            dburl = file.read()
        return App(dburl)


def init_app(cfgpath, dburl, username, email):
    logger.info("Creating dir %s", cfgpath)
    os.makedirs(cfgpath)
    crypto = Crypto(genkeys=True)
    app = App(dburl)
    app.register(str(uuid.uuid4()), username, email, crypto.pubkey, crypto.privkey)


class App(object):

    def __init__(self, dburl: str):
        engine = create_engine(dburl)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.owner = self.session.query(User).filter(id == 1)
        if not self.owner:
            raise Exception("unable to find application owner in database")

    def register(self, uuid: str, username: str, email: str, pubkey: str, privkey: str = None):
        user = User(uuid=uuid, username=username, email=email, pubkey=pubkey, privkey=privkey)
        self.session.add(user)
