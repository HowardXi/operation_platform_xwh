#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/4 17:43
# @Author       : xwh
# @File         : capture_vm.py
# @Description  :

from subprocess import getstatusoutput
from log_configs import log
from asyncio import sleep
from csv import reader
from re import compile
from json import dumps
from settings_parser import cfg
from os.path import exists

sts, txt = getstatusoutput("virsh --version")
if sts != 0:
    log.error("cmd: virsh --version error: %s" % txt)
    exit(-1)
else:
    version = tuple([int(i) for i in txt.strip().replace("\n", "").split(".")])
    if version == (4, 5, 0):
        from client.components.capture_vm.libvirt_4_5 import libvirt as libvirt
        # libvirt = __import__("")
    else:
        log.error("libvirt version error")
        exit(-1)

virt_df_cache_path = "/var/.virt-df"
if not exists(virt_df_cache_path):
    log.error("can not find /var/.virt-df, plz check file or crontab or virt-df")
    exit(-1)


def read_virt_df():
    f = open(virt_df_cache_path, "r")
    rows = reader(f)
    disk_usage = {}
    for row in rows:
        # ['instance-000130b0', '/dev/sda1', '22773', '17407', '4138', '76.4']
        if len(row) != 6 or row[-1][-1] == "%":
            continue
        vm, filesystem, blocks_1k, used, available, use = row
        disk_usage[vm] = float(use) / 100
    return disk_usage


disk_usage = read_virt_df()
conn = libvirt.openReadOnly()
domains = conn.listAllDevices()
infos = []

find_netdev = compile(
    cfg["dev"]["find_netdev_re"].replace("x", "[0-9a-zA-Z]"))


# yum -y install libguestfs-tools libguestfs-xfs virt-top
# virt-df --csv
# Metrics
class VM():
    def __init__(self, domain):
        self.domain = domain
        self.name = self.domain.name()

    @property
    def state(self):
        return self.domain.state()

    @property
    def state_desc(self):
        return vm_status[self.state]

    @property
    async def cpu(self):
        start = domain.getCPUStats(True)
        await sleep(1)
        end = domain.getCPUStats(True)

        return (
                (end["system_time"] - start["system_time"]) +
                (end["user_time"] - start["user_time"]) /
                (end["cpu_time"] - start["cpu_time"]) + 1.0
        )

    def cpu_info(self):
        cpu_time = 0
        system_time = 0
        user_time = 0
        for c in self.domain.getCPUStats(True):
            cpu_time += c["cpu_time"]
            user_time += c["user_time"]
            system_time += c["system_time"]
        return {
            "cpu_time": cpu_time,
            "user_time": user_time,
            "system_time": system_time
        }

    @property
    def memory(self):
        metadata = self.domain.memoryStats()
        return metadata["rss"] / float(metadata["actual"] + 1)

    def memory_info(self):
        metadata = self.domain.memoryStats()
        return {
            "actual": metadata["actual"],
            "rss": metadata["rss"]
        }

    @property
    def disk(self):
        return disk_usage[self.name()]

    @property
    def io(self):
        try:
            rc, rb, wc, wb, _ = self.domain.blockInfo("vda")
            return {
                "read count": rc,
                "read bytes": rb,
                "write count": wc,
                "write bytes": wb
            }
        except Exception as e:
            log.error(str(e))
            return {
                "read count": -1,
                "read bytes": -1,
                "write count": -1,
                "write bytes": -1
            }

    @property
    def network(self):
        d = []
        devs = find_netdev.findall(self.domain.XMLDesc())
        for dev in devs:
            tx_bytes, tx_packets, tx_errors, tx_drop, \
            rx_bytes, rx_packets, rx_errors, rx_drop = self.domain.interfaceStats(dev)
            d.append({
                "tx_bytes": tx_bytes,
                "tx_packets": tx_packets,
                "tx_errors": tx_errors,
                "tx_drop": tx_drop,
                "rx_bytes": rx_bytes,
                "rx_packets": rx_packets,
                "rx_errors": rx_errors,
                "rx_drop": rx_drop,
            })
        return d

    def dump(self):
        return {
            "name": self.name,
            "cpu": self.cpu,
            "disk": self.disk,
            "memory": self.memory,
            "network": self.network,
            "io": self.io
        }
    def __str__(self):
        return dumps(self.dump())


vm_status = {
    0: "no state",
    1: "running",
    2: "blocked on resource",
    3: "paused by user",
    4: "being shut down",
    5: "shut off",
    6: "crashed",
    7: "suspended by guest power management",
    8: "version"
}

info = {
    "name": "",
    "cpu": 0.0,
    "disk": 0.0,
    "memory": 0.0,
    "state desc": "",
    "state code": 0,
    "io": {
        "read": [],
        "write": []
    }
}

for domain in domains:
    state = domain.state()
    name = domain.name()
    uuid = domain.UUIDString()

    cpu = domain.getCPUStats(True)[0]
