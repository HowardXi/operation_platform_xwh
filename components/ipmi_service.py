#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/1 17:20
# @Author  : xwh
# @File    : ipmi.py

import json
from commands import getstatusoutput
from sys import exit
import time
from logging import getLogger
from requests import put
from pymemcache.client import Client
from elasticsearch import Elasticsearch
from init_logger import init_logger
from settings_parser import log_es_addr, ipmi_password, ipmi_username, \
    memcache_addr,zabbix_hostname2ip, translate_host_ip_to_ipmi_ip, send_mail

mem = Client(memcache_addr)
hosts = [zabbix_hostname2ip(host) for host in json.loads(mem.get("host_info")).keys()]
log = getLogger()
#
# if (not ipmi_password) or (not ipmi_username):
#     print -2

# ipmi_addr = trans_addr(ip)


# class log():
#     @staticmethod
#     def error(msg):
#         print msg
#
#     @staticmethod
#     def warning(msg):
#         print msg


# if getstatusoutput("ipmitool -h")[0] != 0:
#     if getstatusoutput("yum install -y ipmitool")[0] != 0:
#         print -3
#         exit(-3)


def get_events(ipmi_ip, user=ipmi_username, pwd=ipmi_password):
    cmd = "ipmitool -H %s -I lanplus -U %s -P %s sel list" % (ipmi_ip, user, pwd)
    events = []
    sts, out = getstatusoutput(cmd)
    # log.warning("call ipmitool code=%s, cmd=%s" % (sts, cmd))
    if sts != 0:
        log.error("call ipmitool error code=%s, cmd=%s, out=%s" % (sts, cmd, out))
        return events
    for line in out.split("\n"):
        event = line.split(" | ")
        if len(event) >= 4:
            id, date, _time, name = event[0:4]
            details = ",".join(event[4:])

            # time_array = time.strptime("%s %s" % (date, _time), "%d/%m/%Y %H:%M:%S")
            # timestamp = int(time.mktime(time_array))
            # struct_time = time.localtime(timestamp)
            # now_time = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
            events.append({
                "id": hex(int(id, 16)),
                # "date": date,
                "host": ipmi_ip,
                # "time": _time,
                "name": name,
                "system log": details,
                "timestamp": time.time(),
                "datetime": "%s %s" % (date, _time)
                # "datetime":time.strftime("%Y-%m-%d %H:%M:%S", struct_time),
            })

        else:
            log.error("ipmi result abnoraml(event info too short): %s, cmd=%s" % (line, cmd))
            continue
    return events


def get_sensor_records(ipmi_ip, user=ipmi_username, pwd=ipmi_password):
    cmd = "ipmitool -H %s -I lanplus -U %s -P %s sdr list" % (ipmi_ip, user, pwd)
    sts, out = getstatusoutput(cmd)
    if sts != 0:
        log.error("call ipmitool error code=%s, cmd=%s, out=%s" % (sts, cmd, out))
        return []
    log.warning("call ipmitool code=%s, cmd=%s" % (sts, cmd))
    sensor_records = []
    for line in out.split("\n"):
        name, value, status = [i.strip() for i in line.split(" | ")]
        if status == "ns":
            continue
        sensor_records.append({
            "name": name,
            "value": value,
            "status": status
        })
    return sensor_records


def pick_not_ok_records(records):
    not_ok = []
    for i in records:
        if i["status"] != "ok":
            not_ok.append(i)
    return not_ok


# def system_log():
#     key = "%s_ipmi_event_num" % ip
#     events = get_events(ipmi_addr)
#     last = json.loads(mem.get(key))
#     if last_num is not None:
#         if len(events) > len(last_num):
#             for
#
#
#     mem.set(key, str(event_num), expire=1200)


struct = {
        "settings": {
            "index": {
                "number_of_replicas": 1,
                "number_of_shards": 1
            }
        },
        "mappings": {
            "values": {
                "properties": {
                    "id": {
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "host": {
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "timestamp": {
                        "type": "long"
                    },
                    "name": {
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "system_log": {
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "datetime": {
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "sensor_status": {
                        "type": "string",
                        "index": "not_analyzed"
                    }
                }
            }
        }
    }


if __name__ == '__main__':
    # TODO write to elasticsearch
    log.warning("start ipmi update hosts=%s" % str(hosts))
    while True:
        for ip in hosts:
            ipmi_ip = translate_host_ip_to_ipmi_ip(ip)
            log.warning("start set %s" % ip)
            mem.set(key=ip + "_ipmi_event", value=json.dumps(get_events(ipmi_ip)),
                    expire=1200)
            log.warning("set %s" % ip + "_ipmi_event")
            sensor_records = get_sensor_records(ipmi_ip)
            mem.set(key=ip + "_ipmi_sensor", value=json.dumps(sensor_records),
                    expire=1200)
            not_oks = pick_not_ok_records(sensor_records)
            log.warning("%s pick not ok: %s" % (ip, json.dumps(not_oks)))
            if not_oks:
                # send_mail(content="ip: %s  sensor records: %s" % (
	            #     ip, json.dumps(not_oks)),
                #       subject_="!!! Cyber Range WARING: IPMI !!!",
                #       target="409356915@qq.com")
                log.warning("ipmi warning %s" % ip)
            log.warning("set %s" % ip + "_ipmi_sensor")



    # print json.dumps(get_sensor_records(trans_addr(ip)), indent=4)
    # key = "%s_ipmi_event_num" % ip
    # event_num = len(get_events(ipmi_addr))
    # last_num = mem.get(key)
    # if last_num is not None:
    #     if event_num > int(last_num):
    #         print json.dumps(
    #             pick_not_ok_records(
    #                 get_sensor_records(ipmi_addr)))
    #         exit(1)
    # print event_num
    # mem.set(key, str(event_num), expire=1200)
    # es = Elasticsearch(log_es_addr)
    # es.update
    # print es.exists("str", "doc")

    # r = put("http://%s/ipmi_data" % log_es_addr,
    #         json=struct, headers={"Content-Type": "application/json"})
    # print r.status_code, r.content

    # es.