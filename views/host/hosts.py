#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/27 10:57
# @Author       : xwh
# @File         : hosts.py
# @Description  : 全部主机ip 名称

from fastapi import APIRouter
from fastapi import Query
from time import time

from utils.prometheus_api import request_prometheus

hosts_router = APIRouter()
HOST_JOB = {
    "compute node", "network node", "controller node", "application node"
}


@hosts_router.get("/")
async def host_base(ip: str =Query(None, max_length=16)):
    """
    物理机基础信息
    """
    all_host = []
    print(ip)
    for host in request_prometheus("", "targets")["activeTargets"]:
        if host["labels"]["job"] in HOST_JOB:
            host_ip = host["labels"]["instance"].split(":")[0]
            print(host_ip)
            if ip:
                if ip == host_ip:
                    all_host.append({
                        "host": host_ip,
                        "health": host["health"],
                        "type": host["labels"]["job"]})

                    # "last_update_time": host["lastScrape"],
                    # "error": host["lastError"],
                    # "last_update_used_time": "%.3f s" % host["lastScrapeDuration"]
            else:
                all_host.append({
                    "host": host_ip,
                    "health": host["health"],
                    "type": host["labels"]["job"]})

    return {
        "status": 0,
        "timestamp": round(time(), 1),
        "msg": "",
        "value": all_host
    }


if __name__ == '__main__':
    from json import dumps
    from asyncio import run

    print(dumps(run(host_base("172.16.0.13")), indent=4))
