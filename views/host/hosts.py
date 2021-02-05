#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/27 10:57
# @Author       : xwh
# @File         : hosts.py
# @Description  : 全部主机ip 名称

from fastapi import APIRouter
from time import time

from utils.prometheus_api import request_prometheus

hosts_router = APIRouter()
HOST_JOB = {
    "compute node", "network node", "controller node", "application node"
}


@hosts_router.get("/")
async def all_host():
    # res =
    all_host = []
    for host in request_prometheus("", "targets")["activeTargets"]:
        if host["labels"]["job"] in HOST_JOB:
            all_host.append({
                "host": host["labels"]["instance"].split(":")[0],
                "health": host["health"],
                "type": host["labels"]["job"]
                # "last_update_time": host["lastScrape"],
                # "error": host["lastError"],
                # "last_update_used_time": "%.3f s" % host["lastScrapeDuration"]
            })
    return {
        "status": 0,
        "timestamp": round(time(), 1),
        "msg": "",
        "value": all_host
    }


if __name__ == '__main__':
    from json import dumps

    print(dumps(all_host(), indent=4))
