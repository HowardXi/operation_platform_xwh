#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/12 17:35
# @Author       : xwh
# @File         : alert.py
# @Description  :
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from utils.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    expr = Column(String(256), nullable=False)
    for_ = Column(String(8), nullable=False)
    costom_label = Column(String(96))
    level = Column(String(10))
    scope = Column(String(32))
    summary = Column(String(128))
    desc = Column(String(256))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

