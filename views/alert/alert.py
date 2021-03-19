#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/12 18:14
# @Author       : xwh
# @File         : alert_rule.py
# @Description  :

from fastapi import APIRouter, Query, Body
from crud.event import *
from crud.alert_rule import create_alert_rule
from pydantic import BaseModel, HttpUrl
from utils.event_handler import send_mail
from typing import List

alert_router = APIRouter()



@alert_router.post("/")
async def add_alert_rule(
        name:str = Body(...),
        group:str = Body(...),
        expr:str = Body(...),
        for_:str = Body(...),
        costom_label:str = Body(""),
        severity:str = Body(...),
        scope:str = Body(None),
        summary:str = Body(...),
        desc:str = Body(...),
):
    """
    添加告警规则 \n
    :param name: 规则名 \n
    :param group: 规则所属组 \n
    :param expr: 规则表达式 \n
    :param for_: 规则在持续多久后告警,格式: 1m 20s 10h \n
    :param costom_label: 自定义标签, 默认为空字符串 \n
    :param severity: 告警等级, 默认为warning \n
    :param scope: 作用域, 对应主机类型或服务名称, 暂时无效,默认为null \n
    :param summary: 告警信息概述 支持prometheus标签 \n
    :param desc: 告警信息详细 支持primetheus标签 \n
    :return: 规则json
    """
    rule = create_alert_rule(
        name, group, expr,for_,costom_label,severity, scope, summary,desc
    )
    return rule.to_dict()



@alert_router.post("/reciver")
async def recv_alert_from_alertmanager(alerts: List = Body(...)):
    """
    给prometheus的告警接受接口,不要调用(暂时不要,除非后期有自定义告警的需求)
    """
    # 如果告警信息的fingerprint已经在库中, 不应再次写入, 具体检查fingerprint

    for alert in alerts:
        fingerprint = alert["fingerprint"]
        old_alert = query_alert_event_by_fingerprint(fingerprint)
        if old_alert.confirm == False or alert.status != old_alert.status:
            send_mail("","")


    pass


@alert_router.get("/confirm")
async def confirm_alert_event(confirmer: str = Query(...), ):
    """
    给告警邮件用的, 也不需要调用
    """
    # 确认后应修改event, 使其不再发送邮件
    pass

