#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/1/27 11:03
# @Author       : xwh
# @File         : prometheus_api.py
# @Description  :

from requests import get, post
from settings_parser import log, prometheus_url
from json import loads
from requests.exceptions import Timeout, ConnectTimeout, ConnectionError


# @log.catch
def _request_prometheus(expr, type, method_func, json_=None):

    url = prometheus_url + "/api/v1/%s" % type + "?query=" + expr
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
    return _request_prometheus(expr, "query", get)

def query_range(expr):
    return _request_prometheus(expr, "query_range", get)

"""
{
	'status': 'success',
	'data': {
		'resultType': 'vector',
		'result': [{
			'metric': {
				'__name__': 'node_disk_io_now',
				'device': 'dm-0',
				'instance': '172.16.0.13:9100',
				'job': '172.16.0.13'
			},
			'value': [1611736943.933, '0']
		}, {
			'metric': {
				'__name__': 'node_disk_io_now',
				'device': 'dm-0',
				'instance': '172.18.0.21:9100',
				'job': '172.18.0.21'
			},
			'value': [1611736943.933, '0']
		}, {
			'metric': {
				'__name__': 'node_disk_io_now',
				'device': 'dm-1',
				'instance': '172.16.0.13:9100',
				'job': '172.16.0.13'
			},
			'value': [1611736943.933, '0']
		}, {
			'metric': {
				'__name__': 'node_disk_io_now',
				'device': 'dm-1',
				'instance': '172.18.0.21:9100',
				'job': '172.18.0.21'
			},
			'value': [1611736943.933, '0']
		}, {
			'metric': {
				'__name__': 'node_disk_io_now',
				'device': 'dm-2',
				'instance': '172.18.0.21:9100',
				'job': '172.18.0.21'
			},
			'value': [1611736943.933, '0']
		}, {
			'metric': {
				'__name__': 'node_disk_io_now',
				'device': 'md126',
				'instance': '172.18.0.21:9100',
				'job': '172.18.0.21'
			},
			'value': [1611736943.933, '0']
		}, {
			'metric': {
				'__name__': 'node_disk_io_now',
				'device': 'md126p1',
				'instance': '172.18.0.21:9100',
				'job': '172.18.0.21'
			},
			'value': [1611736943.933, '0']
		}, {
			'metric': {
				'__name__': 'node_disk_io_now',
				'device': 'md126p2',
				'instance': '172.18.0.21:9100',
				'job': '172.18.0.21'
			},
			'value': [1611736943.933, '0']
		}, {
			'metric': {
				'__name__': 'node_disk_io_now',
				'device': 'md126p3',
				'instance': '172.18.0.21:9100',
				'job': '172.18.0.21'
			},
			'value': [1611736943.933, '0']
		}, {
			'metric': {
				'__name__': 'node_disk_io_now',
				'device': 'md127',
				'instance': '172.18.0.21:9100',
				'job': '172.18.0.21'
			},
			'value': [1611736943.933, '0']
		}, {
			'metric': {
				'__name__': 'node_disk_io_now',
				'device': 'sda',
				'instance': '172.16.0.13:9100',
				'job': '172.16.0.13'
			},
			'value': [1611736943.933, '0']
		}, {
			'metric': {
				'__name__': 'node_disk_io_now',
				'device': 'sda',
				'instance': '172.18.0.21:9100',
				'job': '172.18.0.21'
			},
			'value': [1611736943.933, '0']
		}, {
			'metric': {
				'__name__': 'node_disk_io_now',
				'device': 'sdb',
				'instance': '172.18.0.21:9100',
				'job': '172.18.0.21'
			},
			'value': [1611736943.933, '0']
		}]
	}
}
"""

if __name__ == '__main__':
    pass

