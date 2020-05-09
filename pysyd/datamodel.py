# -*- coding: utf-8 -*-

"""Data Model"""

from sqlalchemy import Column, Integer, String, LargeBinary
from pysyd.database import Base


class User(Base):
    __tablename__ = 'users'

    sid = Column(Integer, primary_key=True, autoincrement=True)  # short internal id
    uid = Column(String, index=True, unique=True)           # UUID
    name = Column(String)
    email = Column(String)
    pubkey = Column(LargeBinary)
    privkey = Column(LargeBinary)

    def __repr__(self):
        return "<User(%s, %s, %s, %s)>" % (self.sid, self.uid, self.name, self.email)


class Dataset(Base):
    __tablename__ = 'dataset'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, index=True, unique=True)
    name = Column(String)   # should be a fully qualified name like com.myorg.data.wheather.rain.2019
    meta = Column(String)   # metadata
    owner = Column(String)  # UID of owner
    file = Column(String)

    def __repr__(self):
        return "<Dataset(%s, %s, %s, %s)>" % (self.sid, self.uid, self.name, self.file)


class Token(Base):
    __tablename__ = 'token'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, index=True, unique=True)
    name = Column(String)
    dataset = Column(String)  # UID of dataset

    def __repr__(self):
        return "<Token(%s, %s, %s)>" % (self.sid, self.uid, self.name)
