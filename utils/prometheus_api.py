#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/27 11:03
# @Author       : xwh
# @File         : prometheus_api.py
# @Description  :

from requests import get, post
from time import time
from json import loads, dumps
from requests.exceptions import Timeout, ConnectTimeout, ConnectionError
from log_configs import log
from settings_parser import cfg


# @log.catch
def request_prometheus(expr, type, method_func=get, **kwargs):
    url = cfg["operation_service_api"]["prometheus_url"] + "/api/v1/"
    if type == "query":
        url += "query?query=" + expr
        param = None
    elif type == "query_range":
        url += "query_range"
        param = {"query": expr, "start": kwargs["start"],
                 "end": kwargs["end"], "step": kwargs["step"]}
    else:
        url += type
        param = None
    try:
        r = method_func(url, timeout=3, params=param)
        log.info("query from prometheus, url=%s, respone=%d" % (url, r.status_code))

        if r.status_code != 200:
            log.error("query error, status_code=%d, content=%s" % (r.status_code, r.content))
            return r.content
        else:
            result = loads(r.content)
            if "status" in result and result["status"] != "success":
                log.error("query error, status_code=%d, content=%s" % (r.status_code, r.content))
                return r.content
            return result["data"]
    except (Timeout, ConnectTimeout, ConnectionError) as e:
        return str(e)
    except Exception as e:
        log.error("query exception, err=%s" % str(e))
        # raise Exception(str(e))


# @log.catch
def query(expr):
    return request_prometheus(expr, "query")


def query_range(expr, start, end, step=60):
    return request_prometheus(expr, type="query_range", start=start, end=end, step=step)


def print_dump(a):
    print(dumps(a, indent=4))


def classify_hosts(job):
    res = []
    for host in request_prometheus("", "targets")["activeTargets"]:
        if host["labels"]["job"] == job:
            res.append(host)
    return res


if __name__ == '__main__':
    print(classify_hosts("kafka"))
    # r =get(prometheus_url + '/api/v1/targets/metadata?match_target={instance="172.16.0.13:9100"}')
    # print(dumps(loads(r.content), indent=4))
    # print_dump(query_range("""sum(increase(node_cpu_seconds_total{mode="idle"}[10m]))"""))
    # now = int(time())
    #
    # print_dump(request_prometheus(
    #     'sum(increase(node_cpu_seconds_total{mode="idle"}',
    #     type="query_range",
    #     from_=now-300, until=now, step=60
    # ))
    # sql = '(1- sum(increase(node_cpu_seconds_total{mode="idle"}[2m])) by (instance)/sum(increase(node_cpu_seconds_total[2m])) by (instance)) * 100'
    # start = now - 600
    # end = now
    #
    # print_dump(request_prometheus(sql, type="query_range", start=start, end=end, step=60))
    # response = requests.get('http://localhost:9090/api/v1/query'),
    # params={'query': "query=container_cpu_load_average_10s{container_name=POD}"})
