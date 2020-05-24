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

    def __init__(self, config=Config):
        db_url = config().db_url
        if db_url == MEMDB_URL:
            self.session = self._create_schema(db_url)
        else:
            self.session = self._open(db_url)

    def get(self, entity, cond) -> Any:
        return self.session.query(entity).filter(cond).scalar()

    def list(self, entity) -> Any:
        return self.session.query(entity).all()

    def add(self, obj) -> Any:
        self.session.add(obj)
        self.session.commit()
        logger.info("%s added to db", obj)
        return obj

    def close(self):
        self.session.close()

    @staticmethod
    def create(db_url):
        if os.path.isfile(db_url.replace('sqlite://', '')):
            raise Exception(f"Database {db_url} already exists")
        Database._create_schema(db_url)

    @staticmethod
    def _open(db_url) -> Session:
        engine = sqlalchemy.create_engine(db_url)
        logger.info(f"Opening {db_url}")
        maker = sessionmaker(bind=engine)
        return maker()

    @staticmethod
    def _create_schema(db_url) -> Session:
        logger.info("Creating schema for %s", db_url)
        engine = sqlalchemy.create_engine(db_url)
        tables = Base.metadata.tables
        Base.metadata.create_all(engine, tables.values(), checkfirst=True)
        logger.debug("creating tables: " + ",".join(k for k in tables.keys()))
        maker = sessionmaker(bind=engine)
        return maker()

