# -*- coding: utf-8 -*-

"""Database Layer"""

import logging
import os
from typing import Any

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pysds.config import Config

# https://github.com/alecthomas/injector
from injector import inject

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    @inject
    def __init__(self, config: Config):
        self.dburl = config.dburl
        if config.setup:
            if os.path.isfile(config.dburl.replace('sqlite://', '')):
                raise Exception("Database " + config.dburl + " already exists")
            logger.info("Creating schema for %s", config.dburl)
            engine = sqlalchemy.create_engine(config.dburl)
            tables = Base.metadata.tables
            Base.metadata.create_all(engine, tables.values(), checkfirst=True)
            logger.debug("creating tables: " + ",".join(k for k in tables.keys()))
        else:
            engine = sqlalchemy.create_engine(self.dburl)
        logger.info("Opening %s", self.dburl)
        maker = sessionmaker(bind=engine)
        self.session = maker()

    def close(self):
        logger.debug("closing session")
        self.session.close()

    def get(self, entity, cond) -> Any:
        return self.session.query(entity).filter(cond).scalar()

    def list(self, entity) -> Any:
        return self.session.query(entity).all()

    def add(self, obj) -> Any:
        self.session.add(obj)
        self.session.commit()
        logger.info("%s added to db", obj)
        return obj
