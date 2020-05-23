# -*- coding: utf-8 -*-

import base64

from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from sqlalchemy.sql import func

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

    def is_admin(self) -> bool:
        return self.privkey is not None


class Dataset(Base):
    """Datasets Metadata (the files are not in database)"""
    __tablename__ = 'dataset'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, index=True, unique=True)
    name = Column(String)   # should be a fully qualified name like com.myorg.data.wheather.rain.2019
    owner = Column(String)  # UUID of owner when imported otherwise owned
    file = Column(String)

    OWNED = 'owned'

    def __repr__(self):
        return f"Dataset({self.sid}, {self.uid}, {self.name}, {self.owner}, {self.file})"

    def is_owned(self) -> bool:
        return self.owner == self.OWNED


class Token(Base):
    """Tokens"""
    __tablename__ = 'token'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, index=True, unique=True)
    name = Column(String)
    dataset = Column(String)    # UUID of dataset
    requester = Column(String)  # UUID of requester
    granter = Column(String)    # UUID of granter
    request_dt = Column(DateTime, default=func.now())
    grant_dt = Column(DateTime)
    grant_status = Column(Integer, default=0)
    locker = Column(LargeBinary)

    def __repr__(self):
        return f"Token({self.sid}, {self.uid}, {self.name})"
