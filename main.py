#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 10:36
# @Author  : xwh
# @File    : main.py

import uvicorn
from settings_parser import cfg
from time import time
from exception import NoExistException

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import http_exception_handler

from views.host.hosts import hosts_router
from views.inventory.hosts import host as inventory_host_router
from views.host.hosts_history import host_history_router
from views.host.hardware import hardware_router
from views.public_service.midware.kafka import kafka_router
from views.function.file_op import file_router
from views.virtual_layer.vm import vm_router
from views.host.ipmi import ipmi_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


# server op
app.include_router(inventory_host_router, prefix="/inventory/host")

# physical layer
app.include_router(hosts_router, prefix="/hosts")
app.include_router(hardware_router, prefix="/hardware")
app.include_router(ipmi_router, prefix="/ipmi")

# virtual layer
app.include_router(vm_router, prefix="/vm")
# app.include_router(vswitch_router,        prefix="/ovs")

app.include_router(host_history_router, prefix="/history")

app.include_router(kafka_router, prefix="/midware/kafka")
app.include_router(file_router, prefix="/function")

if __name__ == '__main__':
    uvicorn.run(
        app='main:app', host="0.0.0.0", port=cfg["operation_service_api"]["listen_port"],
        reload=True, debug=True, )
