#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/1 14:52
# @Author       : xwh
# @File         : file.py
# @Description  : 带进度的文件分发 支持密码 私钥文件 私钥字符串 另外定期检查文件是否过期 过期删除

import paramiko
from functools import partial
from loguru import logger as log
from hashlib import md5
from os.path import getsize
from contextlib import contextmanager
from settings_parser import redis
import time
from fastapi import FastAPI, Request, Form

file_router = FastAPI()


@file_router.post("/file_deliver")
def file_deliver(
        file: str = Form(...),
        hosts: str = Form(...),
        path: str = Form(...),
        password: str = Form(...),
        pkey: str = Form(...)
):
    # Request.json() https://www.cnblogs.com/mazhiyong/p/13345076.html
    log.info("create ssh connection")
    connections = []
    for host in hosts.replace(" ", "").split(","):
        connections.append(FileDeliverHost(host, pwd=password, pkey=pkey))

    log.info("ssh connection done")


@file_router.post("/progress")
def query_file_deliver_progress(host: str, path: str):
    # request = Request.json()
    # host = request["host"]
    # path = request["path"]
    redis.hget("file_deliver", "%s_%s" % (host, path))

    return


class MD5CheckException(Exception):
    pass


class FileDeliverHost():
    def __init__(self, host: str, port=22, user="root", pwd=None, pkey=None):
        log.info("start connect host=%s, pwd=%s" % (host, self.md5sum(pwd or pkey)))
        self.sock = (host, port)
        self.user = user
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=host, port=port, username=user, password=pwd, pkey=pkey)
        self.sftp = self.ssh_client.open_sftp()
        self.open_file_fd = None

    @contextmanager
    def open(self, path, mode):
        self.open_file_fd = self.sftp.open(path, mode=mode, bufsize=paramiko.sftp_file.SFTPFile.MAX_REQUEST_SIZE)
        setattr(self.open_file_fd, "path", path)
        try:
            yield self.open_file_fd
        finally:
            self.open_file_fd.flush()
            self.open_file_fd.close()

    def read(self, n=paramiko.sftp_file.SFTPFile.MAX_REQUEST_SIZE):
        return self.open_file_fd.read(n)

    def write(self, content):
        return self.open_file_fd.write(content)

    def check_md5(self):
        _, stdout, stderr = self.ssh_client.exec_command("md5sum " + self.open_file_fd.path)
        md5_ = str(stdout.read(), encoding="utf-8").split(" ")[0]
        err = str(stderr.read(), encoding="utf-8")
        if len(err):
            raise MD5CheckException(err)
        return self.sock[0], self.open_file_fd.path, md5_

    def close(self):
        if self.open_file_fd:
            try:
                self.open_file_fd.close()
            except Exception as e:
                log.error("close file error: %s" % str(e))
        self.sftp.close()
        self.ssh_client.close()

    def __del__(self):
        self.close()

    def md5sum(self, s):
        if s == None:
            return "None"
        m = md5()
        m.update(bytes(s, encoding="utf-8"))
        return m.hexdigest()


pwd = "h@@T1onZ02Onew"
path = "/root/test.png"


def file_callback(host, remote_path, c, t):
    redis.hset("file_deliver", "%s_%s" % (host, remote_path), value="%2.f" % ((c / t) * 100))
    print("%.2f %%" % ((c / t) * 100))


def task(host_info, local_path, remote_path, callback):
    redis.hset("file_deliver", "%s_%s" % (host_info["host"], remote_path), value="connect host")
    client = FileDeliverHost(host_info["host"], pwd=host_info["pwd"], pkey=host_info["pkey"])
    redis.hset("file_deliver", "%s_%s" % (host_info["host"], remote_path), value="upload")
    client.sftp.put(local_path, remote_path, callback=callback)
    print(host_info["host"] + " done")


if __name__ == '__main__':

    from multiprocessing.pool import Pool
    from multiprocessing import Process

    hosts = ["172.16.0.13", "172.18.0.21"]  # , "172.16.0.17", "172.16.0.16", "172.16.0.18"]
    pwd = "h@@T1onZ02Onew"
    path = "/root/test.png"
    local_path = "../dev/test.gif"
    file_size = getsize(local_path)
    processes = []
    start = time.time()
    for host in hosts:
        name = "%s_%s" % (host, path)
        p = Process(
            target=task,
            args=({
                      "host": host,
                      "pwd": pwd,
                      "pkey": None
                  },
                  local_path, path, partial(file_callback, host, path)),
            name=name
        )
        p.start()
        print("start")
        processes.append((name, p))

    print("use %.2f s" % (time.time() - start))

    print(redis.hget("file_deliver", "172.16.0.13_/root/test.png"))
