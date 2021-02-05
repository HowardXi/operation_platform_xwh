#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/28 14:13
# @Author       : xwh
# @File         : vswitch.py
# @Description  : 动态拓扑信息


# 双网桥(openstack)
# 接口1: vm1      vm2      vm3
# 接口1: nic-mac  nic-mac  nic-mac  [{"name": "vm1", "nic": [{"name": "tapxxxxxxxx-xx", "mac": "xxxxxxxx"}, {}]}]
#        |        |        |
# 接口2:         br-int
#                 |
# 接口2:         br-vlan


# 单网桥(h3c)
# 接口1: vm1      vm2      vm3
# 接口1: nic-mac  nic-mac  nic-mac
#        |        |        |
# 接口2:          br

{"tier0": [{"name": "br-int"}], "tier1": [{"name": "br-vlan"}]}