#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/4 16:18
# @Author       : xwh
# @File         : file_op.py
# @Description  :
from fastapi import APIRouter, UploadFile, File, Form
from requests import post
import time

file_router = APIRouter()

@file_router.get("/file_deliver")
async def file_deliver(
        file: UploadFile = File(...),
        hosts: str = Form(...),
        path: str = Form(...),
        password: str = Form(...),
        pkey: str = Form(...)
):
    start = time.time()
    try:
        res = await file.read()
        with open(file.filename, "wb") as f:
            f.write(res)
        return {"message": "success", 'used_time': time.time() - start,
                'filename': file.filename, "status": 0}
    except Exception as e:
        return {"message": str(e), 'used_time': time.time() - start,
                'filename': file.filename, "status": -1}
