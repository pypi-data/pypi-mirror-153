from __future__ import absolute_import, division, print_function, unicode_literals
# Copyright (C) 2016 Red Hat, Inc.
# python-stqe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-stqe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-stqe.  If not, see <http://www.gnu.org/licenses/>.

"""iscsi.py: Module with test specific method for iSCSI."""

__author__ = "Bruno Goncalves"
__copyright__ = "Copyright (c) 2016 Red Hat, Inc. All rights reserved."

import re  # regex
import libsan.host.iscsi as iscsi
import libsan.host.linux as linux
import libsan.sanmgmt as sanmgmt


def _print(string):
    module_name = __name__
    string = re.sub("DEBUG:", "DEBUG:(" + module_name + ") ", string)
    string = re.sub("FAIL:", "FAIL:(" + module_name + ") ", string)
    string = re.sub("FATAL:", "FATAL:(" + module_name + ") ", string)
    string = re.sub("WARN:", "WARN:(" + module_name + ") ", string)
    print(string)
    if "FATAL:" in string:
        raise RuntimeError(string)
    return


def get_iscsi_conf_host_ifaces():
    """
    Check if server has iSCSI interfaces configured
    If there is no configuration, it should use the default
    Returns:
    \tlist of iSCSI interface information
    """
    obj_sanmgmt = sanmgmt.SanMgmt()
    host_conf = obj_sanmgmt.iscsi_host_conf()
    if not host_conf:
        return None

    if "ifaces" not in host_conf:
        return None

    configured_ifaces = []
    for iface in host_conf["ifaces"].keys():
        if "name" not in host_conf["ifaces"][iface]:
            _print("FAIL: get_iscsi_conf_host_ifaces()- interface defined without name")
            print(host_conf["ifaces"][iface])
            return None
        configured_ifaces.append(host_conf["ifaces"][iface]["name"])
    return configured_ifaces


def get_iscsi_conf_host_portals():
    """
    Check if server has iSCSI interfaces configured
    If there is no configuration, it should use the default
    Returns:
    \tlist of iSCSI interface information
    """
    obj_sanmgmt = sanmgmt.SanMgmt()
    host_conf = obj_sanmgmt.iscsi_host_conf()
    if not host_conf:
        return None

    if "ifaces" not in host_conf:
        return None

    configured_portals = []
    for iface in host_conf["ifaces"].keys():
        iface_info = host_conf["ifaces"][iface]
        if "target_ip" in iface_info and iface_info["target_ip"] not in configured_portals:
            configured_portals.append(iface_info["target_ip"])
    return configured_portals


def get_host_ifaces():
    """
    Return host configured interfaces names. Configures them if needed
    If iSCSI boot will create new interfaces to be used
    """
    # server does not have any interface configured, use default one
    conf_ifaces = get_iscsi_conf_host_ifaces()
    if not conf_ifaces:
        return ["default"]

    is_iscsi_boot = iscsi.is_iscsi_boot()

    all_ifaces = iscsi.get_iscsi_iface_names()

    host_ifaces = []
    for iface in conf_ifaces:
        iface_name = iface["interface_name"]
        # We should not use the iSCSI boot interface for test
        # Exception is qla4xxx interfaces
        if is_iscsi_boot and not re.match("qla4xxx.*", iface_name):
            new_iface = "clone_%s" % iface_name
            if new_iface not in all_ifaces():
                _print("WARN: TODO - Need to clone the interface, and not just create new")
                if not iscsi.create_iscsi_iface(new_iface):
                    _print("FAIL: Could not create %s iface" % new_iface)
                    return None
            iface_name = new_iface

        iface_ip = None
        if "ipv4_address" in iface:
            iface_ip = iface["ipv4_address"]
        # If not IP is set on bnx2i driver we need to enable DHCP
        if re.match("bnx2i.*", iface_name) and not iface_ip:
            iface_ip = "0.0.0.0"

        if iface_ip:
            if not iscsi.iface_set_ip(iface_name, iface_ip):
                _print("FAIL: Could not set IP for iface: %s" % iface_name)
                return None
        host_ifaces.append(iface_name)

    return host_ifaces


def get_host_portals():
    """
    Return a list of host configured portals. If none is set try to use array based on host location
    """
    # server does not have any interface configured, use default one
    conf_portals = get_iscsi_conf_host_portals()
    if conf_portals:
        return conf_portals

    san_conf = sanmgmt.SanMgmt()
    san_conf.load_conf()
    host = linux.hostname()
    if "brq" in host:
        return [san_conf.san_conf_dict["alias"]["ip_brq_equ"]]
    # Use bos array as default
    return [san_conf.san_conf_dict["alias"]["boston_array"]]


def auto_conf(test_type='io_stress'):
    """
    Usage
        auto_conf('test_type')
    Purpose
        Configure iSCSI on generic hosts (not in san_top.conf)
    Parameter
        test_type
    Returns
        scsi_ids   # the iSCSI disks found
            or
        None
    """

    obj_sanmgmt = sanmgmt.SanMgmt()
    host_conf = obj_sanmgmt.iscsi_host_conf()

    linux.install_package("iscsi-initiator-utils")
    iscsi.clean_up()

    iqn_base = 'iqn.1994-05.com.redhat:'
    iqn_tail = None
    arch = linux.os_arch()
    arch = arch.replace('_', '-')

    if test_type == 'io_stress':
        iqn_tail = 'io-stress-tcp-' + arch
        iscsi.set_iscsid_parameter(**{'node.session.cmds_max': '4096', 'node.session.queue_depth': '128'})

    if test_type == 'chap-1way':
        iqn_tail = 'chap-1way-' + arch
        iscsi.set_chap('redhat_out_user', 'redhat_out_pass')

    if test_type == 'chap-2ways':
        iqn_tail = 'chap-2ways-' + arch
        iscsi.set_chap('redhat_out_user', 'redhat_out_pass', 'redhat_in_user', 'redhat_in_pass')

    if test_type == 'big-lun':
        iqn_tail = 'big-lun-' + arch

    if test_type == 'mdadm':
        iqn_tail = 'mdadm-' + arch

    if test_type == 'discard':
        iqn_tail = 'discard-' + arch

    if test_type == 'tcp-general':
        iqn_tail = 'tcp-general-' + arch

    if test_type == 'multipath-io':
        iqn_tail = 'multipath-io-' + arch

    if test_type == 'discovery-many-luns':
        iqn_tail = 'max'

    if test_type == 'os-reboot':
        iqn_tail = 'os-reboot'

    if test_type == 'lsm-test':
        iqn_tail = 'lsm-test-iqn'

    if test_type == 'vdo-general':
        iqn_tail = 'vdo-general'

    if test_type == 'vdo-small':
        iqn_tail = 'vdo-small'

    if test_type == 'stratis-general':
        iqn_tail = 'stratis-general'

    if iqn_tail is None:
        print('FAIL: setup_iscsi(): Wrong test_type')
        return False

    iqn = iqn_base + iqn_tail

    # Lowering iscsid timeout for sessions using multipath
    iscsi.multipath_timeo()

    iface_name = 'default'
    portals = get_host_portals()
    portal = portals[0]

    if host_conf is not None:
        for iface in host_conf["ifaces"].keys():
            iface_ip = None
            subnet_mask = None
            gateway = None

            if "name" in host_conf["ifaces"][iface]:
                iface_name = host_conf["ifaces"][iface]["name"]
            if "target_ip" in host_conf["ifaces"][iface]:
                portal = host_conf["ifaces"][iface]["target_ip"]
            if "ip" in host_conf["ifaces"][iface]:
                iface_ip = host_conf["ifaces"][iface]["ip"]
            if "mask" in host_conf["ifaces"][iface]:
                subnet_mask = host_conf["ifaces"][iface]["mask"]
            if "gateway" in host_conf["ifaces"][iface]:
                gateway = host_conf["ifaces"][iface]["gateway"]
            if test_type == 'io_stress':
                if "iqn" in host_conf["ifaces"][iface]:
                    iqn = host_conf["ifaces"][iface]["iqn"]

            if not discovery_login(iface_name=iface_name, portal=portal, iface_ip=iface_ip, subnet_mask=subnet_mask,
                                   gateway=gateway, iqn=iqn):
                return False

    else:
        if not discovery_login(iface_name=iface_name, portal=portal, iqn=iqn):
            return False

    return True


def discovery_login(iface_name, portal, iqn, iface_ip=None, subnet_mask=None, gateway=None):
    if not iface_name or not portal or not iqn:
        print('FAIL: auto_conf() - Missing iface_name, portal or iqn')
        return False

    if iface_ip:
        if not iscsi.iface_set_ip(iface_name, iface_ip, subnet_mask, gateway):
            _print("FAIL: auto_conf() - Could not set IP for %s" % iface_name)
            return False

    print('INFO: IQN will be set to ' + iqn)

    if not iscsi.iface_set_iqn(iqn, iface_name):
        _print("FAIL: auto_conf() - Could not set %s to iface %s" % (iqn, iface_name))
        return False

    if not iscsi.discovery_st(portal, ifaces=iface_name, disc_db=True):
        print("FAIL: auto_conf() - Could not discover any target on %s using iface %s" % (portal, iface_name))
        return False

    if not iscsi.node_login():
        _print("FAIL: auto_conf() - Could not login to new discovered portal")
        return False
    print("INFO: Iface %s logged in successfully to %s" % (iface_name, portal))

    return True
