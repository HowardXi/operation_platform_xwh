#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/27 11:18
# @Author       : xwh
# @File         : settings_parser.py
# @Description  :

from toml import load
from log_configs import log

setting_file_path = "./settings.toml"
prometheus_url = "http://172.18.0.21:9090"