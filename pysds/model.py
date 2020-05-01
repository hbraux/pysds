# -*- coding: utf-8 -*-

"""Data Model"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, LargeBinary
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html

Base = declarative_base()

class User(Base):
     __tablename__ = 'users'

     id = Column(Integer, primary_key=True, autoincrement=True)
     uuid = Column(String)
     username = Column(String)
     email = Column(String)
     pubkey = Column(LargeBinary)
     privkey = Column(LargeBinary)

     def __repr__(self):
        return "<User(%s,%s,%s)>" % (self.id, self.uuid, self.username)


