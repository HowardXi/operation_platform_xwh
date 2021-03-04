#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/1 16:17
# @Author       : xwh
# @File         : exception.py
# @Description  : 生成prometheus配置文件并重启他,主要是从数据库读取主机信息并配置到prometheus，每次服务开始时调用，

import yaml
from loguru import logger as log
# from settings_parser import prometheus_config_path
from requests import post
import json
from settings_parser import PHYSICAL_HOST_JOB, cfg
from utils.database import SessionLocal
from crud.host import query_all_phy_host


def prometheus_reload():
    prometheus_config_path = "../dev/prometheus.yml"

    with open(prometheus_config_path, "r") as f:
        pc = yaml.load(f, yaml.FullLoader)

    all_phy_host = query_all_phy_host(session=SessionLocal)
    new_scrape_configs = []
    for job in pc["scrape_configs"]:
        if job["job_name"] not in PHYSICAL_HOST_JOB:
            new_scrape_configs.append(job)

    # 先把原本配置中的主机部分删除掉,再重新添加
    pc["scrape_configs"] = new_scrape_configs

    pc["scrape_configs"] = [{
        "job_name": host.node_type,
        "scrape_interval": host.interval,
        "static_configs": [{
            "targets": [
                f"{host.ip}:{host.exporter_port}"
            ],
            "labels": {
                k: v for k, v in json.loads(host.costom_label).values()
            }
        }]
    } for host in all_phy_host]

    with open(prometheus_config_path, "w") as f:
        yaml.safe_dump(pc, f)
    try:
        r = post(cfg["operation_service_api"]["prometheus_url"] + "/-/reload")
        if r.status_code != 200:
            log.error("restart prometheus error: %s" % r.content)
            raise RuntimeError("restart prometheus error: %s" % r.content)
    except Exception as e:
        raise RuntimeError(str(e))

    return pc