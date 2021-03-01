from sqlalchemy.orm import Session
from model.inventory import Host


def create_host(session: Session, ip, node_type):
    host = Host(ip=ip, node_type=node_type, state=1)
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
