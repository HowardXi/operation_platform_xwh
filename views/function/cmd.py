#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/17 16:10
# @Author       : xwh
# @File         : cmd.py
# @Description  :

from fastapi import APIRouter

cmd_router = APIRouter()

@cmd_router.post("/distribute_cmd")
def distribute_cmd(cmd , ips):
    res = {}
    for ip in ips:
        # TODO Host
        host = Host(ip)
        stdout, stderr = host.exec(cmd)
        res.update({
            "host": host,
            "out": stdout.read(),
            "err": stderr.read()
        })
    return