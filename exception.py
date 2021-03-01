#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/1 16:17
# @Author       : xwh
# @File         : exception.py
# @Description  :

from fastapi.exceptions import HTTPException
from fastapi import status

class NoExistException(HTTPException):
    def __init__(
            self,
            detail: str = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BadParamsException():
    def __init__(
            self,
            detail: str = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)