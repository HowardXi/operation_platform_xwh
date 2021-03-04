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
from contextlib import contextmanager

engine = create_engine(
    f'mysql+pymysql://{cfg["db"]["username"]}:{cfg["db"]["password"]}@'
    f'{cfg["db"]["host"]}/operation_platform')
SessionLocal = sessionmaker(bind=engine)

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