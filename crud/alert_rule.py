#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/16 11:18
# @Author       : xwh
# @File         : alert_rule.py
# @Description  :

from sqlalchemy.orm import Session
from model.alertrule import AlertRule
from utils.database import session_maker


def create_alert_rule(
        name, group, expr, for_, costom_label, severity, scope, summary, desc):
    rule = AlertRule(
        name=name,
        group=group,
        expr=expr,
        for_=for_,
        costom_label=costom_label,
        severity=severity,
        scope=scope,
        summary=summary,
        desc=desc
    )
    with session_maker() as s:
        s.add(rule)
        s.commit()
        s.refresh(rule)
    return rule


def delete_alert_rule(name):
    with session_maker() as session:
        rule = session.query(AlertRule).filter(AlertRule.name == name).first()
    return rule


def query_alert_rule(name):
    with session_maker() as session:
        return session.query(AlertRule).filter(AlertRule.name == name).first()


def query_all_alert_rule():
    with session_maker() as session:
        return [rule for rule in session.query(AlertRule)]


if __name__ == '__main__':

    create_alert_rule(
        "mem usage",
        "common group",
        "100-(node_memory_Buffers_bytes+node_memory_Cached_bytes+node_memory_MemFree_bytes)/node_memory_MemTotal_bytes*100 > 60",
        "1m",
        "",
        "warning",
        None,
        "Instance {{ $labels.instance }} 内存使用率过高",
        '''{{ $labels.instance }} of job {{$labels.job}} 内存使用率超过60%,当前使用率 {{ $value | printf "%.2f" }} %.'''

    )
    create_alert_rule(
        "cpu usage",
        "common group",
        '''100-avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) by(instance)*100 > 20''',
        "1m",
        "",
        "warning",
        None,
        "Instance {{ $labels.instance }} cpu使用率过高",
        '''{{ $labels.instance }} of job {{$labels.job}} cpu使用率超过20%,当前使用率 {{ $value | printf "%.2f" }} %.'''

    )

