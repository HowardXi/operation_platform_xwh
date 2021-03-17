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

# 补全 原表达式中{换成{{, }换成}} 以应对str.format的KeyError问题
# 在表达式中用{f}添加条件
expr_map = {
    "single_node": {
        "load1": 'sum(node_load1) by (instance) / count(node_cpu_seconds_total{{mode="system"{f}}}) by (instance)',
        "load15": 'sum(node_load15) by (instance) / count(node_cpu_seconds_total{{mode="system"{f}}}) by (instance)',
        "cpu": '100 * (1 - sum by (instance)(increase(node_cpu_seconds_total{{ mode="idle"{f} }}[5m])) / sum by (instance)(increase(node_cpu_seconds_total[5m])))',
        "mem": '(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes{f}',
        "fs": '(sum(node_filesystem_size_bytes{{device!="rootfs"{f}}}) by (device) - sum('
              'node_filesystem_free_bytes{{device!="rootfs"{f}}}) by (device)) / sum('
              'node_filesystem_size_bytes{{device!="rootfs"{f}}}) by (device)',
        "read_bytes": 'sum(rate(node_disk_read_bytes_total{f}[5m]))by (instance)'

    },
    "cluster": {
        "load1": 'sum(node_load1) by (instance) / count(node_cpu_seconds_total{{mode="system"{f}}}) by (instance)',
        "load15": 'sum(node_load15) by (instance) / count(node_cpu_seconds_total{{mode="system"{f}}}) by (instance)',
        "cpu": '100 * (1 - sum by (instance)(increase(node_cpu_seconds_total{{ mode="idle"{f} }}[5m])) / sum by (instance)(increase(node_cpu_seconds_total[5m])))',
        "mem": '(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes{f}',
        "fs": '(sum(node_filesystem_size_bytes{{device!="rootfs"{f}}}) by (device) - sum('
              'node_filesystem_free_bytes{{device!="rootfs"{f}}}) by (device)) / sum('
              'node_filesystem_size_bytes{{device!="rootfs"{f}}}) by (device)',
        "read_bytes": 'sum(rate(node_disk_read_bytes_total{f}[5m]))by (instance)'


    }
}


@host_metric_router.get("/metric_support_class_")
def show_support_class_():
    """
    这个接口只是为了展示现在支持的class_, 并没有实际作用, 注意分类和接口匹配, 单点对单点接口 集群对集群接口
    """
    return {k: list(v.keys()) for k, v in expr_map.items()}


@host_metric_router.get("/history/cluster/{key}/{value}")
def get_cluster_history(key, value):
    pass


@host_metric_router.get("/latest/cluster/{ip}")
def get_cluster_latest(ip, class_: str = Query(...)):
    pass


@host_metric_router.get("/history/single/{ip}")
def get_single_node_history(ip, class_: str = Query(...), start: int = Query(...),
                            end: int = Query(...), step: int = Query(60, gt=10)):
    """
    物理机的历史使用量信息\n
    start为开始时间 -600表示600秒前\n
    end为结束时间 0 表示现在 -300表示300秒前
    """
    start += int(time())
    end += int(time())

    if start > end:
        raise BadParamsException("请求的时间参数貌似不太对劲")

    if class_ not in expr_map["single_node"]:
        raise NoExistException("不存在这个分类, 支持分类:%s" % str(
            list(expr_map["single_node"].keys())))

    host = query_host(ip)
    if not ip:
        raise NoExistException("没有这个主机%s, 我没查到啊你先看看所有主机里边有没有..., 或者这个主机状态是正常的么" % ip)

    base_expr = expr_map["single_node"][class_]
    f = ',instance="%s:%d"' % (ip, host.exporter_port) if \
        "{{" in base_expr else '{instance="%s:%d"}' % (ip, host.exporter_port)
    expr = base_expr.format(f=f)
    log.info("format expr: %s" % expr)

    res = query_range(expr, start=start, end=end, step=step)["result"]
    if res:
        return res
    else:
        raise NoExistException("没有这样式儿的数据, 我没查到啊")


@host_metric_router.get("/latest/single/{ip}")
def get_single_node_lastest_data(ip, class_: str = Query(...)):
    """
    物理机最新使用量信息
    """
    host = query_host(ip)
    if not ip:
        raise NoExistException("没有这个主机%s, 我没查到啊你先看看所有主机里边有没有..." % ip)

    if class_ not in expr_map["single_node"]:
        raise NoExistException("不存在这个分类, 支持分类:%s" % str(
            list(expr_map["single_node"].keys())))

    base_expr = expr_map["single_node"][class_]
    f = ',instance="%s:%d"' % (ip, host.exporter_port) if \
        "{{" in base_expr else '{instance="%s:%d"}' % (ip, host.exporter_port)
    expr = base_expr.format(f=f)
    # expr = '100 * (1 - sum by (instance)(increase(node_cpu_seconds_total' \
    #        '{mode="idle",instance="172.16.0.13:9100"}[5m])) / sum by ' \
    #        '(instance)(increase(node_cpu_seconds_total[5m])))'
    log.info("format expr: %s" % expr)
    res = query(expr)

    if res:
        return res["result"]
    else:
        raise NoExistException("没有这样式儿的数据, 我没查到啊")


if __name__ == '__main__':
    from asyncio import run

    pass