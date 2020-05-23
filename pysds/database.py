# -*- coding: utf-8 -*-

import logging
import os
from typing import Any

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from pysds.config import Config
from pysds.singleton import Singleton

MEMDB_URL = 'sqlite:///:memory:'

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database(metaclass=Singleton):
    """Small database wrapper on top of SQL Alchemy"""

    def __init__(self):
        self._config = Config()
        self._session = None

    def in_memory(self) -> bool:
        return self._config.db_url() == MEMDB_URL

    def session(self) -> Session:
        if not self._session:
            if self.in_memory():
                self._session = self._create(self._config.db_url())
            else:
                self._session = self._open(self._config.db_url())
        return self._session

    def close(self) -> None:
        logger.debug("closing session")
        self._session.close()

    def get(self, entity, cond) -> Any:
        return self.session().query(entity).filter(cond).scalar()

    def list(self, entity) -> Any:
        return self.session().query(entity).all()

    def add(self, obj) -> Any:
        self.session().add(obj)
        self.session().commit()
        logger.info("%s added to db", obj)
        return obj

    def create(self):
        self._create(self._config.db_url())

    @staticmethod
    def _open(dburl):
        engine = sqlalchemy.create_engine(dburl)
        logger.info(f"Opening {dburl}")
        maker = sessionmaker(bind=engine)
        return maker()

    @staticmethod
    def _create(dburl):
        if os.path.isfile(dburl.replace('sqlite://', '')):
            raise Exception(f"Database {dburl} already exists")
        logger.info("Creating schema for %s", dburl)
        engine = sqlalchemy.create_engine(dburl)
        tables = Base.metadata.tables
        Base.metadata.create_all(engine, tables.values(), checkfirst=True)
        logger.debug("creating tables: " + ",".join(k for k in tables.keys()))
        maker = sessionmaker(bind=engine)
        return maker()
