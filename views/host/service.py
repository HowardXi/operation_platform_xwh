#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/7 10:02
# @Author       : xwh
# @File         : service.py
# @Description  :

from fastapi import APIRouter
from requests import get, post


service_router = APIRouter()

@service_router.get("/status/{name}")
def get_systemd_service_status():
    return
