#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/29 18:27
# @Author       : xwh
# @File         : hosts_metric.py
# @Description  :

from fastapi import APIRouter, Query
from utils.prometheus_api import *
from exception import *
from crud.host import *
from time import time
from dateutil.parser import parse
from settings_parser import cfg
from json import dumps

host_metric_router = APIRouter()

expr_map = {
    "newest": {
        "load1": 'sum(node_load1) by (instance) / count(node_cpu_seconds_total{mode="system"}) by (instance)',
        "load15": 'sum(node_load15) by (instance) / count(node_cpu_seconds_total{mode="system"}) by (instance)',
        "cpu": '100 * (1 - sum by (instance)(increase(node_cpu_seconds_total{{ mode="idle"{f} }}[5m])) / sum by (instance)(increase(node_cpu_seconds_total[5m])))',
        "mem": '(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes',
        "disk": '(sum(node_filesystem_size_bytes{device!="rootfs"{f}}) by (device) - sum(node_filesystem_free_bytes{device!="rootfs"{f}}) by ('
                'device)) / sum(node_filesystem_size_bytes{device!="rootfs"{f}}) by (device)',
        "read_bytes": 'sum(rate(node_disk_read_bytes_total{f}[5m]))by (instance)'

    },
    "history": {
        "cpu": '100 * (1 - sum by (instance)(increase(node_cpu_seconds_total{mode="idle"}[5m])) / sum by ('
               'instance)(increase(node_cpu_seconds_total[5m])))',
    },
    "clus": {}
    # (sum(node_filesystem_size_bytes{device!="rootfs"}) by (device) - sum(node_filesystem_free_bytes{device!="rootfs"}) by (device)) /sum(node_filesystem_size_bytes{device!="rootfs"}) by (device)
}


@host_metric_router.get("/history")
def get_history(host: str, class_: str, start: int, end: int, step: int = 60):
    """
    物理机的历史使用量信息
    """
    if class_ not in expr_map:
        return {
            "status": -1,
            "timestamp": round(time(), 1),
            "msg": f"Unknow type: {class_}, support type: {dumps(list(expr_map.keys()))}",
            "value": {}
        }
    base_expr = expr_map["history"][class_]
    f = ',instance="%s:%d"' % (host, cfg["operation_service_api"]["node_exporter_port"]) if \
        "{" in base_expr else 'instance="%s:%d"' % (host, cfg["operation_service_api"]["node_exporter_port"])
    expr = base_expr.format(f=f)
    log.info("format expr: %s" % expr)
    res = query_range(expr, start=start, end=end, step=step)["result"]
    if res:
        return res
    else:
        raise NoExistException("没有这样式儿的数据, 我没查到啊")


@host_metric_router.get("/latest")
def get_lastest_data(ip: str = Query(...), class_: str = Query(...)):
    """
    物理机最新使用量信息
    """
    host = query_host(ip)
    if not ip:
        raise NoExistException("没有这个主机%s, 我没查到啊" % ip)

    base_expr = expr_map["newest"][class_]
    f = ',instance="%s:%d"' % (ip, host.exporter_port) if \
        "{" in base_expr else '{instance="%s:%d"}' % (ip, host.exporter_port)
    log.info(f)
    log.info("<filter>" in base_expr)
    # expr = base_expr.replace("<filter>", f)
    expr = base_expr.format(f=f)
    # expr = '100 * (1 - sum by (instance)(increase(node_cpu_seconds_total' \
    #        '{mode="idle",instance="172.16.0.13:9100"}[5m])) / sum by ' \
    #        '(instance)(increase(node_cpu_seconds_total[5m])))'
    log.info("format expr: %s" % expr)
    res = query(expr)

    if res:
        return res
    else:
        raise NoExistException("没有这样式儿的数据, 我没查到啊")


if __name__ == '__main__':
    from asyncio import run

    print_dump(query_range(
        expr='(1- sum(increase(node_cpu_sec2onds_total{mode="idle"}[2m])) by (instance)/sum(increase(node_cpu_seconds_total[2m])) by (instance)) * 100',
        start=time() - 600, end=time(), step=60))
