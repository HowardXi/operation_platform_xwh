#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/1 10:37
# @Author       : xwh
# @File         : hardware.py
# @Description  :

from fastapi import APIRouter
from settings_parser import mem
from time import time
import asyncio
from json import loads

hardware_router = APIRouter()

@hardware_router.get("/base/{ip}")
async def host_hardware_info(ip):
    data = loads(mem.get("%s_hardware" % ip) or "{}")
    if data:
        return {
            "status": 0,
            "timestamp": round(time(), 1),
            "msg": "",
            "value": data
        }
    else:
        return {
            "status": -1,
            "timestamp": round(time(), 1),
            "msg": "Can not find host %s" % ip,
            "value": data
        }


if __name__ == '__main__':
    print(asyncio.run(host_hardware_info("172.16.0.13")))
