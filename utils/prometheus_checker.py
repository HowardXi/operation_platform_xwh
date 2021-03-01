#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/1 16:17
# @Author       : xwh
# @File         : exception.py
# @Description  : 生成prometheus配置文件并重启他,主要是从数据库读取主机信息并配置到prometheus，每次服务开始时调用，

from yaml import load
