#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/1 15:49
# @Author       : xwh
# @File         : vm.py
# @Description  :

from fastapi import APIRouter
from settings_parser import mem
from time import time
from datetime import datetime
from json import loads

vm_router = APIRouter()


@vm_router.get("/static_info/{vm_name}")
async def vm_static_info(vm_name):
    vm_data = mem.get(vm_name)
    if vm_data == None:
        return {
            "status": -1,
            "value": None,
            "timestamp": time(),
            "msg": "Can not find %s" % vm_name
        }
    else:
        vm_data = loads(vm_data)
        return {
            "status": 0,
            "timestamp": datetime.fromisoformat(vm_data["cap_time"]).timestamp(),
            "msg": "",
            "value": {
                "name": vm_data["name"],
                "uuid": vm_data["node_id"],
                "capture time": vm_data["cap_time"],
                "instance type": vm_data["instance_type"],
                "vNIC": vm_data["dev"],
                "MAC": vm_data["mac"],
                "metadata": {
                    "nova": {
                        "name": vm_data["nova_name"],
                        "created time": vm_data["creation_time"],
                        "project uuid": vm_data["project_id"],
                        "project name": vm_data["project_name"],
                        "flavor": {
                            "cpu": int(vm_data["quota"]["cpu_limit"].split(" ")[0]),
                            "memory": int(vm_data["quota"]["mem_limit"].split(" ")[0]),
                            "disk": int(vm_data["quota"]["disk_limit"].split(" ")[0]),
                        },
                    }
                }
            }
        }


@vm_router.get("/statistic_info/{vm_name}")
async def statistic_info(vm_name):
    vm_data = mem.get(vm_name)
    if vm_data == None:
        return {
            "status": -1,
            "value": None,
            "timestamp": time(),
            "msg": "Can not find %s" % vm_name
        }
    else:
        vm_data = loads(vm_data)
        return {
            "status": 0,
            "timestamp": datetime.fromisoformat(vm_data["cap_time"]).timestamp(),
            "msg": "",
            "value": {
                "name": vm_data["name"],
                "status": vm_data["status"],
                "status code": vm_data["status_code"],
                "io": {
                    "order": ["Bytes per second", "count per second"],
                    "read": [vm_data["io_speed"]["read_Bps"], vm_data["io_speed"]["read_cps"]],
                    "write": [vm_data["io_speed"]["write_Bps"], vm_data["io_speed"]["write_cps"]],
                },
                "host": vm_data["host_ip"],
                "network": {
                    "upload": round(float(vm_data["traffic"]["upload"].split(" ")[0]), 2),
                    "download": round(float(vm_data["traffic"]["download"].split(" ")[0]), 2)
                },
                "cpu": {
                    "total": vm_data["cpu_details"]["cpu_time"],
                    "user": vm_data["cpu_details"]["user_time"],
                    "system": vm_data["cpu_details"]["system_time"],
                },
                "usage": {
                    "load": float(vm_data["load"].split(" ")[0]),
                    "cpu": float(vm_data["cpu_percent"].split(" ")[0]),
                    "memory": float(vm_data["mem_percent"].split(" ")[0]),
                    "disk": float(vm_data["disk_percent"].split(" ")[0]),
                }

            }
        }
