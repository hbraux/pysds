# -*- coding: utf-8 -*-

import base64

from sqlalchemy import Column, Integer, String, LargeBinary

from pysds.database import Base


class User(Base):
    """Application users. The first User (sid 1) is the local admin"""
    __tablename__ = 'users'

    sid = Column(Integer, primary_key=True, autoincrement=True)  # short internal id
    uid = Column(String, index=True, unique=True)                # UUID
    name = Column(String)
    email = Column(String)
    pubkey = Column(LargeBinary)
    privkey = Column(LargeBinary)

    def __repr__(self):
        return f"User({self.sid}, {self.name}, {self.uid}, {self.email}, {base64.b64encode(self.pubkey).decode()})"


class Dataset(Base):
    """Datasets Metadata (the files are not in database)"""
    __tablename__ = 'dataset'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, index=True, unique=True)
    name = Column(String)   # should be a fully qualified name like com.myorg.data.wheather.rain.2019
    owner = Column(String)  # UUID of owner when imported
    file = Column(String)

    def __repr__(self):
        return f"Dataset({self.sid}, {self.uid}, {self.name}, {self.owner}, {self.file})"


class Token(Base):
    """Tokens"""
    __tablename__ = 'token'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, index=True, unique=True)
    name = Column(String)
    dataset = Column(String)  # UUID of dataset

    def __repr__(self):
        return f"Token({self.sid}, {self.uid}, {self.name})"
