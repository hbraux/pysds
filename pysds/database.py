# -*- coding: utf-8 -*-

"""Database Layer"""

import os
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
        self.config = config
        self.dbfile = "/" + self.config.dbtype + ".db"
        if self.config.dbtype == 'memory':
            self.dburl = 'sqlite:///:memory:'
        else:
            self.dburl = 'sqlite:///' + self.config.path + self.dbfile
        if not os.path.isfile(self.config.path + self.dbfile):
            logger.info("Creating database %s", self.dburl)
            if not os.path.isdir(self.config.path):
                os.makedirs(self.config.path)
            engine = sqlalchemy.create_engine(self.dburl)
            Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)
        else:
            logger.info("Opening database %s", self.dburl)
            engine = sqlalchemy.create_engine(self.dburl)
        maker = sessionmaker(bind=engine)
        self.session = maker()

    def create(self):
        pass

    def get(self, entity, cond) -> Any:
        return self.session.query(entity).filter(cond).scalar()

    def list(self, entity) -> Any:
        return self.session.query(entity).all()

    def add(self, obj) -> Any:
        try:
            self.session.add(obj)
            self.session.commit()
        except Exception as e:
            Status.catched(e)
            logger.error(e)
            return None
        logger.info("%s added to db", obj)
        return obj
