#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/4 17:43
# @Author       : xwh
# @File         : capture_vm.py
# @Description  :

from subprocess import getstatusoutput
from log_configs import log

sts, txt = getstatusoutput("virsh --version")
if sts != 0:
    log.error("cmd: virsh --version error: %s" % txt)
    exit(-1)
else:
    version = tuple([int(i) for i in txt.strip().replace("\n", "").split(".")])
    if version == (4,5,0):
        from .libvirt_4_5 import libvirt as libvirt
    else:
        log.error("libvirt version error")
        exit(-1)

conn = libvirt.openReadOnly()
domains = conn.listAllDevices()
infos = []
# yum -y install libguestfs-tools libguestfs-xfs virt-top
# virt-df --csv
for domain in domains:
    info = {
        "project_id": "",
        "cpu_percent": "",
        "cpu_details": {
            "cpu_time": 0,
            "system_time": 0,
            "user_time": 0
        },
        "mem_percent": "",
        "disk_percent": "",
        "host_ip": "",
        "traffic": {
            "upload": "",
            "download": "",
        },
        "status": -1,
        "status_code":  -1,
        "name": name,
        "creation_time": "",
        "nova_name": "",
        "project_name": "",
        "node_id": vm_id,
        "long_id": vm_id,
        "load": "",
        "io_info": {
            "read_count": 0,
            "read_bytes": 0,
            "write_count": 0,
            "write_bytes": 0
        },
        "io_speed": {
            "read_cps": 0,
            "read_Bps": 0,
            "write_cps": 0,
            "write_Bps": 0
        },
        "instance_type": "kvm",
        "system_type": "",
        "cap_time": "",
        "mac": [],
        "quota": {
            "mem_limit": "-1 Mib",
            "disk_limit": "-1 Gb",
            "cpu_limit": "-1 Core"},
        "dev": []
    }