#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/1 18:01
# @Author       : xwh
# @File         : hosts.py
# @Description  :

from sqlalchemy.orm import Session
from model.inventory import Host
from fastapi import APIRouter, Body, HTTPException
from utils.database import SessionLocal
from utils.prometheus_cfg_reload import prometheus_reload
from crud.host import *

host = APIRouter()

@host.post("/")
def add_host(
        ip: str = Body(..., regex="^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$"),
        node_type: str = Body(..., min_length=1),
        exporter_port: int = Body(..., gt=0),
        interval: str = Body(...),
        physical: bool = Body(True),
        costom_label: str = Body(...),
        desc: str = Body(...),
        ssh_port:int = Body(22),
        ssh_auth_type: str = Body(...),
        ssh_auth: str = Body(...),
        bmc_url: str = Body(None)
    ):
    """
    在资产中添加一个主机  \n
    :param ip: 主机ip \n
    :param node_type: 主机类型或服务名, 如果是[compute node, network node, controller node, application node, operation node]之一,
    则会被认定为是物理服务器, 否则当作服务/虚拟机处理 \n
    :param exporter_port: 主机的采集端口 默认prometheus的node-exporter为9100  \n
    :param interval: 采集间隔 默认60s 支持格式类似"60s", "1h", "5m"  \n
    :param physical: 主机为物理机时为true  \n
    :param costom_label: 自定义主机标签, 值为json字符串, 类似{"key1": "value1", "key2": "value2"}\n
    :param desc: 主机描述信息  \n
    :param ssh_port: ssh端口号, 默认22  \n
    :param ssh_auth_type: ssh认证类型, password或者pkey  \n
    :param ssh_auth: password字符串或者pkey字符串  \n
    :param bmc_url: 主机bmc页面地址  \n
    :return: 主机信息的json  \n
    """
    if query_host(ip):
        raise HTTPException(status_code=400, detail="不能添加重复的host~")
    return create_host(
        ip=ip, node_type=node_type, exporter_port=exporter_port,interval=interval,
        physical=physical, costom_label=costom_label, desc=desc, ssh_port=ssh_port,
        ssh_auth_t=ssh_auth_type, ssh_auth=ssh_auth, bmc_url=bmc_url)

@host.delete("/")
def add_host(
        ip: str = Body(..., regex="^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$", embed=True),
    ):
    if not query_host(ip):
        raise HTTPException(status_code=400, detail="没有这个host~")
    return delete_host(ip=ip)

@host.post("/reload")
def reload_prometheus():
    """
    主机添加完毕之后重载prometheus配置
    """
    prometheus_reload()
    return ""

