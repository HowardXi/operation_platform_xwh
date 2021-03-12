#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/3/1 16:17
# @Author       : xwh
# @File         : exception.py
# @Description  : 生成prometheus配置文件并重启他,主要是从数据库读取主机信息并配置到prometheus，每次服务开始时调用，

import yaml
from loguru import logger as log
from requests import post
import json
from collections import defaultdict
from settings_parser import PHYSICAL_HOST_JOB, cfg
from crud.host import query_all_host


def prometheus_generate_config():
    prometheus_config_path = "../dev/prometheus.yml"

    with open(prometheus_config_path, "r") as f:
        pc = yaml.load(f, yaml.FullLoader)

    all_host = query_all_host(False)
    new_scrape_configs = []
    # for job in pc["scrape_configs"]:
    #     if job["job_name"] not in PHYSICAL_HOST_JOB:
    #         new_scrape_configs.append(job)

    # 先把原本配置中的主机部分删除掉,再重新添加
    pc["scrape_configs"] = new_scrape_configs
    # print(json.dumps(pc["scrape_configs"]))
    class_hosts = defaultdict(list)
    for host in all_host:
        class_hosts[host.node_type].append(host)

    for class_, hosts in class_hosts.items():
        pc["scrape_configs"].append({
            "job_name": f"{class_}",
            "scrape_interval": "60s",
            "static_configs": [{
                "targets": [f"{host.ip}:{host.exporter_port}" for host in hosts],
            }]
        })

    print(json.dumps(pc["scrape_configs"], indent=4))
    with open(prometheus_config_path, "w") as f:
        yaml.safe_dump(pc, f)
    return pc


def prometheus_reload():
    try:
        r = post(cfg["operation_service_api"]["prometheus_url"] + "/-/reload")
        log.info("prometheus reload configure, code=%s, content=%s." % (
            r.status_code, r.content))
        if r.status_code != 200:
            log.error("restart prometheus error: %s" % r.content)
            raise RuntimeError("restart prometheus error: %s" % r.content)
    except Exception as e:
        raise RuntimeError(str(e))


if __name__ == '__main__':
    prometheus_reload()
