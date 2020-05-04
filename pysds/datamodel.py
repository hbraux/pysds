# -*- coding: utf-8 -*-

"""Data Model"""

# because of metadata, the data model depends upon sqlalchemy types
from sqlalchemy import Column, Integer, String, LargeBinary
from database import Base


class User(Base):
    __tablename__ = 'users'

    sid = Column(Integer, primary_key=True, autoincrement=True)  # short internal id
    uid = Column(String, index=True, unique=True)                # unique id
    name = Column(String)
    email = Column(String)
    pubkey = Column(LargeBinary)
    privkey = Column(LargeBinary)

    def __repr__(self):
        return "<User(%s, %s, %s, %s)>" % (self.sid, self.name, self.email, self.uid)


class Dataset(Base):
    __tablename__ = 'dataset'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, index=True, unique=True)
    name = Column(String)  # should be a fully qualified name like com.myorg.data.wheather.rain.2019
    desc = Column(String)
    owner = Column(String)
    file = Column(String)

    def __repr__(self):
        return "<Dataset(%s, %s, %s)>" % (self.sid, self.name, self.uid)
