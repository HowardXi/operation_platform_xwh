#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/29 18:27
# @Author       : xwh
# @File         : host.py
# @Description  :

from fastapi import APIRouter

host_router = APIRouter()

@host_router.get("/hello")
async def hello():
    return "hello"