#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/27 11:08
# @Author       : xwh
# @File         : log_configs.py
# @Description  :

from loguru import logger
from platform import platform
from pathlib import Path

if platform().startswith("Linux"):
    log_dir = '/var/log/operation_service_x'
    path = Path(log_dir)
    if not path.exists():
        path.mkdir(parents=True)
    logger.add('operation_service_{time}.log', rotation='00:00',
               retention='15 days', compression="tar.gz")

log = logger

if __name__ == '__main__':
    print(platform())
