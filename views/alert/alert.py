#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/12 18:14
# @Author       : xwh
# @File         : alert.py
# @Description  :

from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
from typing import List

alert_router  = APIRouter()



@alert_router.post("/")
async def recv_alert_from_alertmanager():

    pass
