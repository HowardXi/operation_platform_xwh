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
    ip = Column(String(16), index=True)
    # job = Column(String) # "compute node", "network node", "controller node", "application node", "operation node"
    exporter_port = Column(Integer, default=9100)
    interval = Column(String(6), default="60s")
    physical = Column(Boolean)  # physical or virtual
    node_type = Column(String(24))
    costom_label = Column(String(96))
    state = Column(Integer, default=0)
    description = Column(String(96))

    ssh_port = Column(Integer, default=22)
    ssh_auth_type = Column(String(10)) # choice pkey or password
    ssh_auth = Column(String(256)) # pkey conetnt or password content

    bmc_url = Column(String(128))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class NetworkDevice(Base):
    __tablename__ = "network_device"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String(16), index=True, nullable=True)
    name = Column(String(32), nullable=False)
    state = Column(Integer, default=0)
    dev_type = Column(String(16), default="switch") # "switch", "router", "hardware(ids etc.)"
    description = Column(String(128))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), unique=True, index=True)
    description = Column(String(128))
    health_uri = Column(String(128))
    host = Column(String(16), nullable=False)
    port = Column(Integer, nullable=False)



if __name__ == '__main__':
    print(Host(
        ip="1234",
        node_type="test",
        state=0
    ).to_dict())
