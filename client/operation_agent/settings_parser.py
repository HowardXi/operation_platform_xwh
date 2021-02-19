#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/27 11:18
# @Author       : xwh
# @File         : settings_parser.py
# @Description  :

from yaml import safe_load as load
from json import dumps
from log_configs import log
from redis import ConnectionPool, Redis
import sys
from psutil import cpu_count
from pymemcache.client import PooledClient as MemClient
import os

work_dir = os.path.dirname(os.path.abspath(__file__))
settings_file_path = os.path.join(work_dir,"settings.yml")

def load_cfg():
    try:
        with open(settings_file_path, "r", encoding="utf-8") as f:
            c = load(f.read())
        log.info("load configure. current content=%s" % dumps(c))
        return c
    except Exception as e:
        log.error("load cfg error: %s " % str(e))


cfg = load_cfg()

# print(mem.get("172.16.0.13_ipmi_sensor"))
