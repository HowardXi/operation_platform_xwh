#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2021/2/2 14:40
# @Author       : xwh
# @File         : system_service_status.py
# @Description  :

from loguru import logger as log
from dbus import SystemBus, SessionBus, Interface, exceptions
from systemd import journal

DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'
SYSTEMD_BUSNAME = 'org.freedesktop.systemd1'
SYSTEMD_PATH = '/org/freedesktop/systemd1'
SYSTEMD_MANAGER_INTERFACE = 'org.freedesktop.systemd1.Manager'
SYSTEMD_UNIT_INTERFACE = 'org.freedesktop.systemd1.Unit'


class SystemdBus(object):
    def __init__(self, user=False):
        self.bus = SessionBus() if user else SystemBus()
        systemd = self.bus.get_object(SYSTEMD_BUSNAME, SYSTEMD_PATH)
        self.manager = Interface(systemd, dbus_interface=SYSTEMD_MANAGER_INTERFACE)

    def get_unit_active_state(self, unit):
        unit = self.manager.LoadUnit(unit)
        unit_object = self.bus.get_object(SYSTEMD_BUSNAME, unit)
        unit_properties = Interface(unit_object, DBUS_INTERFACE)
        return unit_properties.Get(SYSTEMD_UNIT_INTERFACE, 'ActiveState')

    def get_unit_field_state(self, unit, field):
        unit = self.manager.LoadUnit(unit)
        unit_object = self.bus.get_object(SYSTEMD_BUSNAME, unit)
        unit_properties = Interface(unit_object, DBUS_INTERFACE)
        return unit_properties.Get(SYSTEMD_UNIT_INTERFACE, field)

    def get_unit_load_state(self, unit):
        unit = self.manager.LoadUnit(unit)
        unit_object = self.bus.get_object(SYSTEMD_BUSNAME, unit)
        unit_properties = Interface(unit_object, DBUS_INTERFACE)
        return unit_properties.Get(SYSTEMD_UNIT_INTERFACE, 'LoadState')

    def reload(self):
        self.manager.Reload()

    # In [31]: manager.DisableUnitFiles(["zabbix-agent.service"], False)
    # Out[31]: dbus.Array([dbus.Struct((dbus.String(u'unlink'), dbus.String(u'/etc/systemd/system/multi-user.target.wants/zabbix-agent.service'), dbus.String(u'')), signature=None)], signature=dbus.Signature('(sss)'))


    # In [33]: manager.EnableUnitFiles(["zabbix-agent.service"], False, True)
    # Out[33]:
    # (dbus.Boolean(True),
    #  dbus.Array([dbus.Struct((dbus.String(u'symlink'), dbus.String(u'/etc/systemd/system/multi-user.target.wants/zabbix-agent.service'), dbus.String(u'/usr/lib/systemd/system/zabbix-agent.service')), signature=None)], signature=dbus.Signature('(sss)')))

    def start_unit(self, unit):
        try:
            self.manager.StartUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

    def stop_unit(self, unit):
        try:
            self.manager.StopUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

    def restart_unit(self, unit):
        try:
            self.manager.RestartUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

    def reload_unit(self, unit):
        try:
            self.manager.ReloadUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

    def reload_or_restart_unit(self, unit):
        try:
            self.manager.ReloadOrRestartUnit(unit, 'replace')
            return True
        except exceptions.DBusException:
            return False

class Journal(object):
    def __init__(self, unit):
        self.reader = journal.Reader()
        self.reader.add_match(_SYSTEMD_UNIT=unit)

    def get_tail(self, lines):
        self.reader.seek_tail()
        self.reader.get_previous(lines)
        journal_lines = ['{__REALTIME_TIMESTAMP} {MESSAGE}'.format(**value) for value in self.reader]
        self.reader.close()
        return journal_lines


if __name__ == '__main__':
    service = "zabbix-agent.service"
    s = systemdBus()
    s.get_unit_load_state(service) # service status
    # s.get_unit_field_state("zabbix-agent.service", "ActiveEnterTimestamp").variant_level
    j = Journal(service)
    j.get_tail(10) # service log tail 10 lines


