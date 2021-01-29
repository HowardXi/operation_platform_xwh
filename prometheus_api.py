#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/27 11:03
# @Author       : xwh
# @File         : prometheus_api.py
# @Description  :

from requests import get, post
from settings_parser import log, prometheus_url
from json import loads, dumps
from requests.exceptions import Timeout, ConnectTimeout, ConnectionError


# @log.catch
def request_prometheus(expr, type, method_func=get, json_=None):
    url = prometheus_url + "/api/v1/%s" % type
    if expr:
        url += "?query=" + expr
    try:
        r = method_func(url, timeout=3, json=json_)
        log.info("query from prometheus, url=%s, respone=%d" % (url, r.status_code))

        if r.status_code != 200:
            log.error("query error, status_code=%d, content=%s" % (r.status_code, r.content))
            return False, r.content
        else:
            result = loads(r.content)
            if "status" in result and result["status"] != "success":
                log.error("query error, status_code=%d, content=%s" % (r.status_code, r.content))
                return False, r.content
            return True, result["data"]
    except (Timeout, ConnectTimeout, ConnectionError) as e:
        return False, str(e)
    except Exception as e:
        log.error("query exception, err=%s" % str(e))
        # raise Exception(str(e))


# @log.catch
def query(expr):
    return request_prometheus(expr, "query", get)


def query_range(expr):
    return request_prometheus(expr, "query_range", get)

def print_dump(a):
    print(dumps(a, indent=4))

if __name__ == '__main__':
    # r =get(prometheus_url + '/api/v1/targets/metadata?match_target={instance="172.16.0.13:9100"}')
    # print(dumps(loads(r.content), indent=4))
    print_dump(request_prometheus("", "targets")[1])