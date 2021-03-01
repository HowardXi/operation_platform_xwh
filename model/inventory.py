#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/1 17:49
# @Author       : xwh
# @File         : inventory.py
# @Description  :

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from utils.database import Base


class Host(Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip = Column(String, unique=True, index=True)
    job = Column(String) #
    part = Column(String) # physical，
    node_type = Column(String)
    state = Column(Integer, default=0)


    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Switch(Base):
    __tablename__ = "switches"

    id = Column(Integer, primary_key=True, index=True)
    # ip = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    state = Column(Integer, default=0)


    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}




if __name__ == '__main__':
    print(Host(
        ip="1234",
        node_type="test",
        state=0
    ).to_dict())