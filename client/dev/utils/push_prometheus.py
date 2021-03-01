#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/7 10:26
# @Author       : xwh
# @File         : push_prometheus.py
# @Description  :

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

