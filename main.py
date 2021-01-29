#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 10:36
# @Author  : xwh
# @File    : main.py

import uvicorn
from fastapi import FastAPI
from views.hosts import hosts_router
from views.host import host_router

app = FastAPI()
app.include_router(hosts_router, prefix="/hosts")
app.include_router(host_router, prefix="/host")

if __name__ == '__main__':
    uvicorn.run(
        app='main:app', host="127.0.0.1", port=8000,
        reload=True, debug=True, )