# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer

from pysds.database import Base


class DatabaseSample(Base):
    __tablename__ = 'database_sample'

    sid = Column(Integer, primary_key=True, autoincrement=True)

