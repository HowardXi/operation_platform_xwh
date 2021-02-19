#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/7 10:33
# @Author       : xwh
# @File         : cache_data.py
# @Description  :

from settings_parser import cfg
from loguru import logger
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from redis import Redis, ConnectionPool
from psutil import cpu_count
from pymemcache.client import PooledClient
from time import time

registry = CollectorRegistry()
log = logger


def push_data(instance, class_, host, value: float):
    g = Gauge(class_, 'virtual machine statistic data', labelnames=("instance_name", "class", "instance"), registry=registry)
    g.labels(instance, "usage", host).set(value)
    push_to_gateway('172.18.0.21:9091', job='vm_metrics', registry=registry)

push_data("xxxxxx", "cpu_usage", "", 90.212)

#
mem = PooledClient((cfg["memcache"]["host"], cfg["memcache"]["port"]), max_pool_size=cpu_count() * 2) \
    if cfg["operation_agent"]["data_target"]["memcache"] else None

if cfg["operation_agent"]["data_target"]["redis"]:
    redis_pool = ConnectionPool(host=cfg["redis"]["host"], port=cfg["redis"]["port"],
                                password=cfg["redis"]["password"], decode_responses=True)
    redis = Redis(connection_pool=redis_pool)
else:
    redis = None

def set(instance, class_,value):
    if mem:
        mem.set(instance + "_" + class_, value, expire=180)
        log.info(f"set memcache: key={instance + '_' + class_}, value={value}")

    if redis:
        redis.hset(instance, class_, value=value, )
