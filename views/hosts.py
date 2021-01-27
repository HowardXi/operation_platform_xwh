#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/27 10:57
# @Author       : xwh
# @File         : hosts.py
# @Description  :

from router import router

@router.get("hosts")
def get_all_host():
    return