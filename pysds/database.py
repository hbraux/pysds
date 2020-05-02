# -*- coding: utf-8 -*-

"""Database Layer"""

import logging
import os
from typing import Any

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from errors import application_error
from singleton import Singleton
from config import Config

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database(metaclass=Singleton):

    def __init__(self, config=None):
        self.config = config or Config()
        dbfile = "/" + self.config.dbtype  + ".db"
        if self.config.dbtype == 'memory':
            dburl = 'sqlite:///:memory:'
        else:
            dburl = 'sqlite:///' + self.config .path + dbfile
        if not os.path.isfile(self.config .path + dbfile):
            logger.info("Creating database %s", dburl)
            if not os.path.isdir(self.config .path):
                os.makedirs(self.config .path)
            engine = sqlalchemy.create_engine(dburl)
            Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)
        else:
            logger.info("Using database %s", dburl)
            engine = sqlalchemy.create_engine(dburl)
        self._session = sessionmaker(bind=engine)()

    def get(self, entity, sid=None, uid=None) -> Any:
        return self._session.query(entity).filter('sid' == sid)

    def add(self, obj) -> bool:
        try:
            self._session.add(obj)
            self._session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return application_error(e)
        logger.info("%s added to db", obj)
        return True
