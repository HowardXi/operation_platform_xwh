#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/16 11:26
# @Author       : xwh
# @File         : event.py
# @Description  :
from sqlalchemy.orm import Session
from model.alertrule import AlertEvent
from utils.database import session_maker
from settings_parser import PHYSICAL_HOST_JOB


def create_alert_event(
        name, status, fingerprint, confirm, confirm_user, ):
    alert_event = AlertEvent(
        name, status, fingerprint, confirm, confirm_user,)
    with session_maker() as s:
        s.add(alert_event)
        s.commit()
        s.refresh(alert_event)
    return alert_event


def delete_alert_event(name):
    with session_maker() as session:
        alert_event = session.query(AlertEvent).filter(AlertEvent.name == name).first()
    return alert_event


def query_alert_event_by_name(name):
    with session_maker() as session:
        return session.query(AlertEvent).filter(AlertEvent.name == name).first()


def query_alert_event_by_fingerprint(fingerprint):
    with session_maker() as session:
        return session.query(AlertEvent).filter(AlertEvent.fingerprint == fingerprint).first()


def confirm_alert_event_by_fingerprint(fingerprint, confirmer):
    with session_maker() as session:
        event = session.query(AlertEvent).filter(AlertEvent.fingerprint == fingerprint).first()
        event.confirm = True
        event.confirmer = confirmer
        session.commit()


def query_all_alert_event():
    with session_maker() as session:
        return [alert_event for alert_event in session.query(AlertEvent)]


if __name__ == '__main__':
    from utils.database import *

    # print(query_alert_event("172.16.0.13"))
    print(query_alert_event("test"))
