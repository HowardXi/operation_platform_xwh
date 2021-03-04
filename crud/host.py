from sqlalchemy.orm import Session
from model.inventory import Host
from settings_parser import PHYSICAL_HOST_JOB


def create_host(
        session: Session, ip, node_type, exporter_port, interval, physical,
        costom_label, desc, ssh_auth_t, ssh_auth, ssh_port, bmc_url):
    host = Host(
        ip=ip, node_type=node_type, state=1,
        exporter_port=exporter_port, physical=physical,
        costom_label=costom_label, description=desc,
        interval=interval, ssh_auth=ssh_auth, ssh_auth_type=ssh_auth_t,
        ssh_port=ssh_port, bmc_url=bmc_url
    )
    session.add(host)
    session.commit()
    session.refresh(host)
    return host


def delete_host(session: Session, ip):
    host = session.query(Host).filter(Host.ip == ip).first()
    session.delete(host)
    session.commit()
    session.refresh(host)
    return host


def update_host(session: Session, ip, state):
    host = session.query(Host).filter(Host.ip == ip).first()
    host.state = state
    session.commit()
    session.refresh(host)
    return host


def query_host(session: Session, ip):
    return session.query(Host).filter(Host.ip == ip).first()

def query_all_phy_host(session: Session):
    res = []
    for host in session.query(Host):
        if host.node_type in PHYSICAL_HOST_JOB:
            res.append(host)

    return res

