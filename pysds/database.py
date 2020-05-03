# -*- coding: utf-8 -*-

"""Database Layer"""

import logging
import os
from typing import Any

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from status import Status
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
        maker = sessionmaker(bind=engine)
        self._session = maker()

    def get(self, entity, cond) -> Any:
        return self._session.query(entity).filter(cond).scalar()

    def list(self, entity) -> Any:
        return self._session.query(entity).all()

    def add(self, obj) -> Any:
        try:
            self._session.add(obj)
            self._session.commit()
        except Exception as e:
            return Status.catched(e, logger)
        logger.info("%s added to db", obj)
        return obj
