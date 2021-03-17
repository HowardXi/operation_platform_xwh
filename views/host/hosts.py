#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/27 10:57
# @Author       : xwh
# @File         : hosts.py
# @Description  : 全部主机ip 名称

from fastapi import APIRouter
from fastapi import Query
from time import time
from settings_parser import PHYSICAL_HOST_JOB
from utils.prometheus_api import request_prometheus

hosts_router = APIRouter()


@hosts_router.get("/")
async def host_base(ip: str = Query(None, max_length=16), job: str = Query(None)):
    """
    物理机状态信息和基础信息
    """
    all_host = []
    for host in request_prometheus("", "targets")["activeTargets"]:
        if host["labels"]["job"] in PHYSICAL_HOST_JOB:
            host_ip = host["labels"]["instance"].split(":")[0]
            if ip and not job:
                if ip == host_ip:
                    all_host.append({
                        "host": host_ip,
                        "health": host["health"],
                        "job": host["labels"]["job"],
                        "last_update_time": host["lastScrape"],
                        "error": host["lastError"],
                        "last_update_used_time": "%.3f s" % host["lastScrapeDuration"]})

            if job and not ip:
                if job == host["labels"]["job"]:
                    all_host.append({
                        "host": host_ip,
                        "health": host["health"],
                        "job": host["labels"]["job"],
                        "last_update_time": host["lastScrape"],
                        "error": host["lastError"],
                        "last_update_used_time": "%.3f s" % host["lastScrapeDuration"]})

            if job and ip:
                if job == host["labels"]["job"] and ip == host_ip:
                    all_host.append({
                        "host": host_ip,
                        "health": host["health"],
                        "job": host["labels"]["job"],
                        "last_update_time": host["lastScrape"],
                        "error": host["lastError"],
                        "last_update_used_time": "%.3f s" % host["lastScrapeDuration"]})

            # else:
            #     all_host.append({
            #         "host": host_ip,
            #         "health": host["health"],
            #         "job": host["labels"]["job"],
            #         "last_update_time": host["lastScrape"],
            #         "error": host["lastError"],
            #         "last_update_used_time": "%.3f s" % host["lastScrapeDuration"]})

    return all_host



if __name__ == '__main__':
    from json import dumps
    from asyncio import run

    print(dumps(request_prometheus("", "targets")["activeTargets"], indent=4))
