#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/12 17:35
# @Author       : xwh
# @File         : alert.py
# @Description  :
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from utils.database import Base


class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    group = Column(String(32), nullable=False)
    expr = Column(String(256), nullable=False)
    for_ = Column(String(8), nullable=False)
    costom_label = Column(String(96), default="")
    severity = Column(String(10))
    scope = Column(String(32))
    summary = Column(String(128))
    desc = Column(String(256))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AlertEvent(Base):
    __tablename__ = "alert_event"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    status = Column(String(12), nullable=False)
    fingerprint = Column(String(16), nullable=False, index=True)
    # 生成的邮件中应该带有一个url可以进行告警确认, url中应带有确认者的信息, 确认后的告警不再发送邮件
    confirm = Column(Boolean(), default=False)
    confirm_user = Column(String(64))



