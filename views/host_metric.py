#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 10:52
# @Author  : xwh
# @File    : host_metric.py
# @Desc    : 物理机cpu 内存 硬盘 等指标

from router import router

@router.get("/host_name")
def get_host_name():
    pass