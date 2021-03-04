#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/28 14:14
# @Author       : xwh
# @File         : kafka.py
# @Description  :

from utils.prometheus_api import classify_hosts, query
from fastapi import APIRouter, Query
from loguru import logger
from exception import NoExistException
from time import time

log = logger

kafka_router = APIRouter()


@kafka_router.get("/")
async def hello():
    return "hello"


@kafka_router.get("/hosts")
async def kafka_hosts(ip:str = Query(None)):
    res= []
    for host in classify_hosts("kafka"):
        host_ip = host["labels"]["instance"].split(":")[0]
        if ip:
            if ip == host_ip:
                res.append({
                    "host": host_ip,
                    "health": host["health"],
                    "last_update_time": host["lastScrape"],
                })
        else:
            res.append({
                "host": host_ip,
                "health": host["health"],
                "last_update_time": host["lastScrape"],
            })
    return res


@kafka_router.get("/consumergroup_lag")
async def kafka_consumergroup_lag():
    res = []
    for i in query("kafka_consumergroup_lag")["result"]:
        res.append({
            "consumergroup": i["metric"]["consumergroup"],
            "partition": i["metric"]["partition"],
            "topic": i["metric"]["topic"],
            "lag": int(i["value"][1]),
            "datetime": i["value"][0]
            # datetime.datetime.fromtimestamp(int(i["value"][0])).isoformat("T")
        })
    return {
        "status": 0,
        "timestamp": round(time(), 1),
        "msg": "",
        "value": res
    }


@kafka_router.get("/{ip}")
async def kafka_info(ip):
    res = {}
    print(classify_hosts("kafka"))
    for i in classify_hosts("kafka"):
        if ip == i["labels"]["instance"].split(":")[0]:
            return i
    if res:
        return {
            "status": 0,
            "timestamp": round(time(), 1),
            "msg": "",
            "value": res
        }
    else:
        raise NoExistException("找不着这个Kafka的broker, 先看看有没有添加这个主机/服务")



if __name__ == '__main__':
    from json import dumps
    from asyncio import run

    print(query("kafka_consumergroup_lag"))
