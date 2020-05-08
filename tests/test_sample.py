# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String

from database import Base


class Sample(Base):
    __tablename__ = 'sample'

    sid = Column(Integer, primary_key=True, autoincrement=True)

