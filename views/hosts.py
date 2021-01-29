#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/27 10:57
# @Author       : xwh
# @File         : hosts.py
# @Description  : 全部主机ip 名称

from fastapi import APIRouter

from prometheus_api import request_prometheus, query

hosts_router = APIRouter()
HOST_JOB = {
    "compute node", "network node", "controller node", "application node"
}


@hosts_router.get("/all")
async def get_all_host():
    # res =
    all_host = []
    for host in request_prometheus("", "targets")[1]["activeTargets"]:
        if host["labels"]["job"] in HOST_JOB:
            all_host.append({
                "host": host["labels"]["instance"].split(":")[0],
                "health": host["health"],
                "type": host["labels"]["job"]
                # "last_update_time": host["lastScrape"],
                # "error": host["lastError"],
                # "last_update_used_time": "%.3f s" % host["lastScrapeDuration"]
            })
    return all_host


@hosts_router.get("/{ip}")
async def host_details(ip):
    for host in request_prometheus("", "targets")[1]["activeTargets"]:
        if host["labels"]["instance"].split(":")[0] == ip:
            return {
                "host": host["labels"]["instance"].split(":")[0],
                "health": host["health"],
                "type": host["labels"]["job"],
                "last_update_time": host["lastScrape"],
                "error": host["lastError"],
                "last_update_used_time": "%.3f s" % host["lastScrapeDuration"]
            }
    return request_prometheus("", "targets")[1]["activeTargets"]


if __name__ == '__main__':
    from json import dumps

    print(dumps(host_details("172.16.0.13"), indent=4))
