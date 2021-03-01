#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/29 18:27
# @Author       : xwh
# @File         : hosts_history.py
# @Description  :

from fastapi import APIRouter
from utils.prometheus_api import *
from time import time
from dateutil.parser import parse
from settings_parser import cfg
from json import dumps

host_history_router = APIRouter()

expr_map = {
    "cpu": '(1- sum(increase(node_cpu_seconds_total{mode="idle"{f}}[2m])) by (instance)/sum(increase(node_cpu_seconds_total[2m])) by (instance)) * 100'
}


@host_history_router.get("/{host}")
def get_history(host: str, type_: str, start: int, end: int, step: int = 60):
    """
    物理机的历史使用量信息
    """
    if type_ not in expr_map:
        return {
            "status": -1,
            "timestamp": round(time(), 1),
            "msg": f"Unknow type: {type_}, support type: {dumps(list(expr_map.keys()))}",
            "value": {}
        }
    base_expr = expr_map[type_]
    expr = base_expr.format(f=',instance="%s:%d"' % (
        host, cfg["operation_service_api"]["node_exporter_port"]))
    res = query_range(expr, start=start, end=end, step=step)["result"]
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
            "msg": f"no such data, expr: {expr}",
            "value": res
        }


if __name__ == '__main__':
    from asyncio import run

    print_dump(query_range(
        expr='(1- sum(increase(node_cpu_sec2onds_total{mode="idle"}[2m])) by (instance)/sum(increase(node_cpu_seconds_total[2m])) by (instance)) * 100',
        start=time() - 600, end=time(), step=60))
