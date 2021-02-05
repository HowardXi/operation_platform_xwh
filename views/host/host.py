#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/29 18:27
# @Author       : xwh
# @File         : host.py
# @Description  :

from fastapi import APIRouter
from utils.prometheus_api import *
from time import time
from dateutil.parser import parse
from settings_parser import cfg

host_router = APIRouter()
host_history_router = APIRouter()

expr_map = {
    "cpu": '(1- sum(increase(node_cpu_seconds_total{mode="idle"{f}}[2m])) by (instance)/sum(increase(node_cpu_seconds_total[2m])) by (instance)) * 100'
}


@host_history_router.get("/{host}/{type}}/{start}/{end}/{step}")
def get_history(host, type_, start, end, step=60):
    if type_ not in expr_map:
        return {
            "status": -1,
            "timestamp": round(time(), 1),
            "msg": "Unknow type: %s" % type_,
            "value": {}
        }
    expr = expr_map[type_]
    res = query_range(
        expr.format(f=',instance="%s:%d"' % (
            host, cfg["operation_service_api"]["node_exporter_port"])),
        start=start, end=end, step=step)["result"]
    if res:
        return {
            "status": 0,
            "timestamp": round(time(), 1),
            "msg": "",
            "value": res
        }
    else:
        return {
            "status": -1,
            "timestamp": round(time(), 1),
            "msg": "no such data",
            "value": res
        }


@host_router.get("/{ip}")
async def base_info(ip):
    print(request_prometheus("", "targets"))
    for host in request_prometheus("", "targets")["activeTargets"]:
        if host["labels"]["instance"].split(":")[0] == ip:
            return {
                "status": 0,
                "timestamp": round(parse(host["lastScrape"]).timestamp(), 1),
                "msg": "",
                "value": {
                    "host": host["labels"]["instance"].split(":")[0],
                    "health": host["health"],
                    "type": host["labels"]["job"],
                    "last_update_time": host["lastScrape"],
                    "error": host["lastError"],
                    "last_update_used_time": "%.3f s" % host["lastScrapeDuration"]
                }
            }
    return {
        "status": -1,
        "timestamp": round(time(), 1),
        "msg": "Can not find host %s" % ip,
        "value": {}
    }


if __name__ == '__main__':
    from asyncio import run

    print_dump(query_range(
        expr='(1- sum(increase(node_cpu_sec2onds_total{mode="idle"}[2m])) by (instance)/sum(increase(node_cpu_seconds_total[2m])) by (instance)) * 100',
        start=time() - 600, end=time(), step=60))
