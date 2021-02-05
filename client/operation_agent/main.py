#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/2 17:51
# @Author       : xwh
# @File         : main.py
# @Description  :
from fastapi import FastAPI
import uvicorn

router = FastAPI()

if __name__ == '__main__':
    uvicorn.run(
        app='main:app', host="127.0.0.1", port=10011,
        reload=True, debug=True, )