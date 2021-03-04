#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/1 17:47
# @Author       : xwh
# @File         : database.py
# @Description  :

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings_parser import cfg


engine = create_engine(
    f'mysql+pymysql://{cfg["db"]["username"]}:{cfg["db"]["password"]}@'
    f'{cfg["db"]["host"]}/operation_platform')
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

if __name__ == '__main__':
    print(engine)
    print(SessionLocal)