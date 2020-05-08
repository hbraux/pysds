# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer

from pysds.database import Base


class Sample(Base):
    __tablename__ = 'sample'

    sid = Column(Integer, primary_key=True, autoincrement=True)
