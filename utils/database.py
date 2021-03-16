#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/1 17:47
# @Author       : xwh
# @File         : database.py
# @Description  :

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from settings_parser import cfg
from contextlib import contextmanager

engine = create_engine(
    f'mysql+pymysql://{cfg["db"]["username"]}:{cfg["db"]["password"]}@'
    f'{cfg["db"]["host"]}/operation_platform')
# 注意mysql默认字符集

# db_url = {
#     'database': cfg["db"]["db_name"],
#     'drivername': 'mysql',
#     'username': cfg["db"]["username"],
#     'password': cfg["db"]["password"],
#     'host': cfg["db"]["host"],
#     'query': {'charset': 'utf8'},
# }
# engine = create_engine(URL(**db_url), encoding="utf8")

SessionLocal = sessionmaker(bind=engine,expire_on_commit=False)

Base = declarative_base()

Base.metadata.create_all(engine)

@contextmanager
def session_maker(session=SessionLocal()):
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == '__main__':
    print(engine)
    print(SessionLocal)