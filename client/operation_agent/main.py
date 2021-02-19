#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/2 17:51
# @Author       : xwh
# @File         : main.py
# @Description  : 数值数据发到prometheus pushgateway 方便作图 , 字符串数据放redis 不需要历史数据

from fastapi import FastAPI
import uvicorn

router = FastAPI()

if __name__ == '__main__':
    uvicorn.run(
        app='main:app', host="127.0.0.1", port=10011,
        reload=True, debug=True, )