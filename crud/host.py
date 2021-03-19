from sqlalchemy.orm import Session
from model.inventory import Host
from utils.database import session_maker
from settings_parser import PHYSICAL_HOST_JOB


def create_host(
        ip, node_type, exporter_port, interval, physical,
        costom_label, desc, ssh_auth_t, ssh_auth, ssh_port, bmc_url):
    host = Host(
        ip=ip, node_type=node_type, state=1,
        exporter_port=exporter_port, physical=physical,
        costom_label=costom_label, description=desc,
        interval=interval, ssh_auth=ssh_auth, ssh_auth_type=ssh_auth_t,
        ssh_port=ssh_port, bmc_url=bmc_url
    )
    with session_maker() as s:
        s.add(host)
        s.commit()
        s.refresh(host)
    return host


def delete_host(ip, node_type):
    with session_maker() as session:
        host = session.query(Host).filter(Host.ip == ip, Host.node_type == node_type).first()
    return host


def update_host(ip, state):
    with session_maker() as session:
        host = session.query(Host).filter(Host.ip == ip).first()
        host.state = state
        session.commit()
    return host


def query_host(ip):
    with session_maker() as session:
        return session.query(Host).filter(Host.ip == ip).first()


def query_all_host(_phy=True):
    with session_maker() as session:
        res = []
        for host in session.query(Host):
            if _phy == True:
                if host.node_type in PHYSICAL_HOST_JOB:
                    res.append(host)
            else:
                res.append(host)

    return res


if __name__ == '__main__':
    from utils.database import *

    # print(query_host("172.16.0.13"))
    create_host(
        "172.16.0.16",
        "compute node",
        9100,
        "1m",
        True,
        None,
        "test desc",
        "pwd",
        "testpwd",
        22,
        "test"
    )
