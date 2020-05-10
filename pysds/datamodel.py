# -*- coding: utf-8 -*-

"""Data Model"""
import base64

from sqlalchemy import Column, Integer, String, LargeBinary

from pysds.database import Base


class User(Base):
    __tablename__ = 'users'

    sid = Column(Integer, primary_key=True, autoincrement=True)  # short internal id
    uid = Column(String, index=True, unique=True)           # UUID
    name = Column(String)
    email = Column(String)
    pubkey = Column(LargeBinary)
    privkey = Column(LargeBinary)

    def __repr__(self):
        return f"User({self.sid}, {self.name}, {self.uid}, {self.email}, {base64.b64encode(self.pubkey).decode()})"


class Dataset(Base):
    __tablename__ = 'dataset'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, index=True, unique=True)
    name = Column(String)   # should be a fully qualified name like com.myorg.data.wheather.rain.2019
    owner = Column(String)  # UID of owner when imported
    file = Column(String)

    def __repr__(self):
        return f"Dataset({self.sid}, {self.uid}, {self.name}, {self.owner}, {self.file})"


class Token(Base):
    __tablename__ = 'token'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, index=True, unique=True)
    name = Column(String)
    dataset = Column(String)  # UID of dataset

    def __repr__(self):
        return f"Token({self.sid}, {self.uid}, {self.name})"
