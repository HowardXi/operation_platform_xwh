#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/1 18:01
# @Author       : xwh
# @File         : hosts.py
# @Description  :

from sqlalchemy.orm import Session
from model.inventory import Host
from fastapi import APIRouter

host = APIRouter()

@host.post("/")
def add_host():


