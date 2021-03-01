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
from crud.host import *

host = APIRouter()

@host.post("/")
def add_host(
        ip: str = Body(..., regex="^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$", embed=True),
        node_type: str = Body(..., ge=0, lt=5, embed=True), # TODO 复合节点？
    ):
    if query_host(SessionLocal, ip):
        raise HTTPException(status_code=400, detail="不能添加重复的host~")
    return create_host(SessionLocal, ip=ip, node_type=node_type)

@host.delete("/")
def add_host(
        ip: str = Body(..., regex="^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$", embed=True),
    ):
    if not query_host(SessionLocal, ip):
        raise HTTPException(status_code=400, detail="没有这个host~")
    return delete_host(SessionLocal, ip=ip)



