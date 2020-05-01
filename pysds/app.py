# -*- coding: utf-8 -*-

"""Application core"""
import base64
import os
import logging
import uuid
from typing import ByteString

import sqlalchemy
import sqlalchemy.orm

from pysds.crypto import Crypto
from pysds.model import User, Base

CFG_FILE = "/app.cfg"
DEFAULT_USER = os.environ.get('USER')
DEFAULT_EMAIL = DEFAULT_USER + "@email.org"

logger = logging.getLogger(__name__)

class App(object):

    def  __init__(self, path='~/.sds', dbtype='sqlite', rsabits=2048):
        self.path = os.path.expanduser(path)
        if dbtype == 'memory':
            self.dburl = 'sqlite:///:memory:'
        else:
            self.dburl = 'sqlite:///' + path + "/app.db"
        self.session = None
        self.rsabits = rsabits

    def open(self) -> bool:
        if not os.path.isfile(self.path + CFG_FILE):
            return False
        if not self.session:
            self._open_session()
        return True

    def setup(self, username=DEFAULT_USER, email=DEFAULT_EMAIL):
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        self._open_session(create_schema=True)
        crypto = Crypto(nbbits=self.rsabits)
        uid = str(uuid.uuid4())
        self.owner = self.register(uid, username, email, crypto.pubkey, crypto.privkey)
        with open(self.path + CFG_FILE, mode='w') as f:
            f.write("url=" + self.dburl)
        logging.info("Application ready")

    def register(self, uid: str, username: str, email: str, pubkey: ByteString, privkey: ByteString = None):
        pubbytes = pubkey
        if type(pubkey) is str:
            logger.debug("converted public key from Bytes64 string to bytes")
            pubbytes = base64.b64decode(pubkey)
        user = User(uuid=uid, username=username, email=email, pubkey=pubbytes, privkey=privkey)
        self.session.add(user)
        self.session.commit()
        logging.info("User registered %s", user)

    # PRIVATE METHODS

    def _open_session(self, create_schema=False):
        engine = sqlalchemy.create_engine(self.dburl)
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        self.session = Session()
        if create_schema:
            logging.info("Creating database %s", self.dburl)
            Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)
        else:
            self.owner = self.session.query(User).filter(id == 1)
            if not self.owner:
                raise Exception("unable to find default user in database")
