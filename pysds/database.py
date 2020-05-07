# -*- coding: utf-8 -*-

"""Database Layer"""

import logging
from typing import Any

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from status import Status
from config import Config

# https://github.com/alecthomas/injector
from injector import inject

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    @inject
    def __init__(self, config: Config):
        self.dburl = config.dburl
        self._session = None
        self._engine = None

    def create(self):
        logger.info("Creating schema for %s", self.dburl)
        self._engine = sqlalchemy.create_engine(self.dburl)
        tables = Base.metadata.tables
        Base.metadata.create_all(self._engine, tables.values(), checkfirst=True)
        logger.debug("creating tables: " + ",".join(k for k in tables.keys()))

    def session(self):
        if not self._session:
            logger.info("Opening %s", self.dburl)
            if not self._engine:
                self._engine = sqlalchemy.create_engine(self.dburl)
            maker = sessionmaker(bind=self._engine)
            self._session = maker()
        return self._session

    def close(self):
        self.session().close()

    def get(self, entity, cond) -> Any:
        return self.session().query(entity).filter(cond).scalar()

    def list(self, entity) -> Any:
        return self.session().query(entity).all()

    def add(self, obj) -> Any:
        try:
            self.session().add(obj)
            self.session().commit()
        except Exception as e:
            Status.catched(e)
            logger.error(e)
            return None
        logger.info("%s added to db", obj)
        return obj
