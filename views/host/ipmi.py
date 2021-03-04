#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/1 15:47
# @Author       : xwh
# @File         : ipmi.py
# @Description  :

from fastapi import APIRouter, Query
from exception import NoExistException
from settings_parser import mem
from json import loads
from time import time

ipmi_router = APIRouter()

@ipmi_router.get("/sensor/")
async def get_sensor_data(ip:str = Query(...)):
    data = loads(mem.get("%s_ipmi_sensor" % ip) or "{}")
    if data:
        return {
            "status": 0,
            "timestamp": round(time(), 1),
            "msg": "",
            "value": data
        }
    else:
        raise NoExistException("Can not find IPMI sensor data about host %s" % ip)


if __name__ == '__main__':
    get_sensor_data("172.16.0.13")