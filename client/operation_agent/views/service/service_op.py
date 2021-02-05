#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/2 17:56
# @Author       : xwh
# @File         : service_op.py
# @Description  :

from fastapi import FastAPI
from .system_service_status import SystemdBus, Journal

service = FastAPI()

@service.get("/status/{name}")
async def get_service_status(name):
    dbus = SystemdBus()
    state = dbus.get_unit_field_state(name, "ActiveState")
    return {
        "name": name,
        "ActiveState": state
    }

@service.get("/{behavior}/{str:name}")
async def service_operate(behavior, name):
    if behavior not in {"restart", "start", "stop"}:
        return "Unsupport"
    dbus = SystemdBus()
    support = {
        "restart": dbus.restart_unit,
        "start": dbus.start_unit,
        "stop": dbus.stop_unit,
    }
    return support[behavior](name)
