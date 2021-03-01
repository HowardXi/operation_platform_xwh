#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/1 10:37
# @Author       : xwh
# @File         : hardware.py
# @Description  :

from fastapi import APIRouter
from settings_parser import mem
from exception import NoExistException
from time import time
import asyncio
from json import loads

hardware_router = APIRouter()

@hardware_router.get("/hardware")
async def host_hardware_info(ip=None):
    data = loads(mem.get("%s_hardware" % ip) or "{}")
    if data:
        return {
            "status": 0,
            "timestamp": round(time(), 1),
            "msg": "",
            "value": data
        }
    else:
        raise NoExistException("不知道你请求这玩意在哪, 查查url和缓存吧")


if __name__ == '__main__':
    print(asyncio.run(host_hardware_info("172.16.0.13")))
