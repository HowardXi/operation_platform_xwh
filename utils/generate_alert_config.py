#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/12 18:13
# @Author       : xwh
# @File         : generate_alert_config.py
# @Description  :


import yaml
from loguru import logger as log
from crud.alert_rule import *
import json
from collections import defaultdict

def generate_prometheus_alert_config():
    cfg = {
        "groups": []
    }
    group = defaultdict(list)

    for i in query_all_alert_rule():
        group[i.group].append(i)

    for group_name, rules in group.items():
        body = {
            "name": group_name,
            "rules": []
        }
        for rule in rules:
            laber = {
                "severity": rule.severity
            }
            if rule.costom_label:
                laber.update(json.loads(rule.costom_laber))
            body["rules"].append({
                "alert": rule.name,
                "expr": rule.expr,
                "for": rule.for_,
                "labels": laber,
                "annotations": {
                    "summary": rule.summary,
                    "description": rule.desc
                }
            })
        cfg["groups"].append(body)
    return cfg


if __name__ == '__main__':
    prometheus_config_path = "../dev/prometheus_alert_rule_example.yml"

    # print(json.dumps(generate_prometheus_alert_config(), indent=4))
    with open("../dev/generate_prometheus_alert_config.yml", "w+",encoding="utf-8") as f:
        yaml.dump(generate_prometheus_alert_config(), f, allow_unicode=True,default_flow_style=False)
    # with open(prometheus_config_path, "rb") as f:
    #     pc = yaml.load(f, yaml.FullLoader)
    #     print(json.dumps(pc, indent=4))