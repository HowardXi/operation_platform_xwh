#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/12 18:14
# @Author       : xwh
# @File         : alert.py
# @Description  :

from fastapi import APIRouter, Query, Body
from crud.event import *
from pydantic import BaseModel, HttpUrl
from utils.event_handler import send_mail
from typing import List

alert_router = APIRouter()



@alert_router.post("/")
async def create_alert_rule():
    pass



@alert_router.post("/reciver")
async def recv_alert_from_alertmanager(alerts: List = Body(...)):
    # 如果告警信息的fingerprint已经在库中, 不应再次写入, 具体检查fingerprint
    # 如果状态或者指纹二者之一发生变化 就认为是不同的event 需要重新发送邮件



    for alert in alerts:
        fingerprint = alert["fingerprint"]
        old_alert = query_alert_event_by_fingerprint(fingerprint)
        if old_alert.confirm == False:
            send_mail("","")


    pass


@alert_router.get("/confirm")
async def confirm_alert_event(confirmer: str = Query(...), ):
    # 确认后应修改event, 使其不再发送邮件
    pass

