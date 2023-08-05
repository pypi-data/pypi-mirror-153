#!/usr/bin/python -u

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
#
# Author: Bruno Goncalves   <bgoncalv@redhat.com>

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
import libsan.host.scsi as scsi
import libsan.host.iscsi as iscsi
import libsan.host.mp as mp
import libsan.host.fc as fc
import libsan.host.net as net
import libsan.sanmgmt as sanmgmt
import libsan.host.linux as linux
import libsan.host.dt as dt
import libsan.misc.array as array
import stqe.host.nfs_lock as nfs_lock
import stqe.host.LogChecker as log
import libsan.misc.time
import re
import sys
import os
import argparse

obj_sanmgmt = None

opt_failover_mode = None
opt_max_interval = None
opt_max_flap_uptime = None
opt_max_flap_downtime = None
opt_max_flap_count = None
opt_dt_time = None

all_supported_failover_methods = ["sa_ctrler_reboot", "fc_target",
                                  "physw_flap_target", "physw_target",
                                  "physw_flap_host", "physw_host",
                                  "iscsi_session", "sysfs",
                                  "fc_host", "iscsi_host"]

_check_method_to_func = {}


def _print(string):
    module_name = __name__
    string = re.sub("DEBUG:", "DEBUG:(" + module_name + ") ", string)
    string = re.sub("FAIL:", "FAIL:(" + module_name + ") ", string)
    string = re.sub("FATAL:", "FATAL:(" + module_name + ") ", string)
    string = re.sub("WARN:", "WARN:(" + module_name + ") ", string)
    print(string)
    sys.stdout.flush()
    if "FATAL:" in string:
        raise RuntimeError(string)
    return


def _check_failover_iscsi_session(mpath):
    """
    """
    if not mpath:
        _print("FAIL: _check_failover_iscsi_session() - requires mpath_name parameter")
        return None

    _print("DEBUG: _check_failover_iscsi_session() - mpath %s" % mpath)
    mp_info = mp.multipath_query_all(mpath)

    if "disk" not in mp_info:
        _print("FAIL: _check_failover_iscsi_session() - %s has no SCSI disk" % mpath)
        return None

    iscsi_sessions = iscsi.query_all_iscsi_sessions()
    if not iscsi_sessions:
        return None
    failover_option_list = []
    for scsi_disk in mp_info["disk"].keys():
        for ses in iscsi_sessions.keys():
            if "disks" not in iscsi_sessions[ses]:
                continue
            if scsi_disk in iscsi_sessions[ses]["disks"]:
                iface = iscsi_sessions[ses]["iface"]
                t_iqn = iscsi_sessions[ses]["t_iqn"]
                persist_ip = iscsi_sessions[ses]["persist_ip"]
                failover_option = "-T %s -p %s -I %s" % (t_iqn, persist_ip, iface)
                failover_option_list.append(failover_option)

    failover_option_list = array.dedup(failover_option_list)
    if len(failover_option_list) < 2:
        _print("WARN: There is less than 2 iSCSI sessions running on %s" % mpath)
        return None
    return failover_option_list


def _check_failover_sysfs(mpath_name):
    """
    Usage
      check_failover_sysfs(mpath_name)
    Purpose
      Check whether all the disks has this sysfs file:
          /sys/block/sdX/device/state
    Parameter
      mpath_name     # like 'mpathb'
    Returns
      failover_entries
          or
      None
    """
    if not mpath_name:
        _print("FAIL: _check_failover_sysfs() - requires mpath_name parameter")
        return None

    _print("DEBUG: _check_failover_sysfs() - mpath %s" % mpath_name)
    disks = mp.get_disks_of_mpath(mpath_name)
    if not disks:
        return None

    if len(disks) < 2:
        _print("FAIL: %s has less then 2 paths, we won't run sysfs failover" % mpath_name)
        print(disks)
        return None

    failure = False
    for disk in disks:
        path = "/sys/block/%s/device/state" % disk
        if not os.path.isfile(path):
            failure = True
            _print("FAIL: %s  has not sysfs file: %s" % (disk, path))

    if failure:
        _print("FAIL: check_failover_sysfs(): Multipath %s has some disk "
               + "does not have /sys/block/sdX/device/state file" % mpath_name)
        return None

    return disks


def _check_failover_fc_host(mpath_name):
    """
    Usage
      check_failover_fc_host(mpath_name)
    Purpose
      Check whether switches which connected HBA ports is controlable.
    Parameter
      mpath_name     # like 'mpathb'
    Returns
      failover_entries
          or
      None
    """
    if ("FC" not in mp.transport_types_of_mpath(mpath_name) and
            "FCoE" not in mp.transport_types_of_mpath(mpath_name)):
        return None

    return _check_failover_switch(mpath_name=mpath_name,
                                  flag_host=True, flag_physw=False)


def _check_failover_fc_target(mpath_name):
    """
    Usage
      _check_failover_fc_target(mpath_name)
    Purpose
      Check whether switches which connected Target port is controlable.
    Parameter
      mpath_name     # like 'mpathb'
    Returns
      failover_entries
          or
      None
    """
    if ("FC" not in mp.transport_types_of_mpath(mpath_name) and
            "FCoE" not in mp.transport_types_of_mpath(mpath_name)):
        return None

    return _check_failover_switch(mpath_name=mpath_name,
                                  flag_host=False, flag_physw=False)


def _check_failover_physw_host(mpath_name):
    """
    Usage
      check_failover_physw_host(mpath_name)
    Purpose
      Check whether physical switch which connected HBA ports is controlable.
    Parameter
      mpath_name     # like 'mpathb'
    Returns
      failover_entries
          or
      None
    """
    return _check_failover_switch(mpath_name=mpath_name,
                                  flag_host=True, flag_physw=True)


def _check_failover_physw_target(mpath_name):
    """
    Usage
      _check_failover_physw_target(mpath_name)
    Purpose
      Check whether physical switches which connected Target port is controlable.
    Parameter
      mpath_name     # like 'mpathb'
    Returns
      failover_entries
          or
      None
    """
    return _check_failover_switch(mpath_name=mpath_name,
                                  flag_host=False, flag_physw=True)


def _check_failover_iscsi_host(mpath_name):
    """
    Usage
      check_failover_iscsi_host(mpath_name)
    Purpose
      Check whether switches which connected HBA ports is controlable.
    Parameter
      mpath_name     # like 'mpathb'
    Returns
      failover_entries
          or
      None
    """
    if "iSCSI" not in mp.transport_types_of_mpath(mpath_name):
        return None

    return _check_failover_switch(mpath_name=mpath_name,
                                  flag_host=True, flag_physw=False)


def _check_failover_sa_ctrler_reboot(mpath_name):
    """
    """
    global obj_sanmgmt

    if not mpath_name:
        _print("FAIL: _check_failover_sa_ctrler_reboot() - requires mpath_name parameter")
        return None

    mp_t_wwpns = mp.t_wwpns_of_mpath(mpath_name)
    if not mp_t_wwpns:
        _print("FAIL: _check_failover_sa_ctrler_reboot() - Did not find target WWPN for %s" % mpath_name)
        return None

    sa_t_wwpn_2_ctrler = obj_sanmgmt.sa_t_wwpn_2_ctrler()
    if not sa_t_wwpn_2_ctrler:
        _print("FAIL: _check_failover_sa_ctrler_reboot() - Did not find target WWPN on target controllers")
        return None

    if len(sa_t_wwpn_2_ctrler) < 2:
        _print("FAIL: _check_failover_sa_ctrler_reboot() - Storage array has only 1 controller")
        print(sa_t_wwpn_2_ctrler)
        return None

    t_wwpns = []
    mp_ctrlers = []  # ctrlers used by mpath
    for ctrler in sa_t_wwpn_2_ctrler.keys():
        for t_wwpn in sa_t_wwpn_2_ctrler[ctrler]:
            if t_wwpn not in mp_t_wwpns:
                # Skip t_wwpn if it is not used by multipath device
                continue
            if t_wwpn not in t_wwpns:
                t_wwpns.append(t_wwpn)
            if ctrler not in mp_ctrlers:
                mp_ctrlers.append(ctrler)

    if len(mp_ctrlers) < 2:
        _print(
            "FAIL: _check_failover_sa_ctrler_reboot() - mpath %s is connected to less then 2 controllers" % mpath_name)
        return None

    if len(t_wwpns) < 2:
        _print(
            "FAIL: _check_failover_sa_ctrler_reboot() - "
            "Despite having more then 1 controller, we found less then 2 target WWPNs")
        print(t_wwpns)
        return None

    return t_wwpns


# This dict should be defined after all _check_failover'method' functions are defnied
_check_method_to_func["iscsi_session"] = _check_failover_iscsi_session
_check_method_to_func["iscsi_host"] = _check_failover_iscsi_host
_check_method_to_func["sysfs"] = _check_failover_sysfs
_check_method_to_func["fc_host"] = _check_failover_fc_host
_check_method_to_func["fc_target"] = _check_failover_fc_target
_check_method_to_func["physw_host"] = _check_failover_physw_host
_check_method_to_func["physw_target"] = _check_failover_physw_target
_check_method_to_func["physw_flap_host"] = _check_failover_physw_host
_check_method_to_func["physw_flap_target"] = _check_failover_physw_target
_check_method_to_func["sa_ctrler_reboot"] = _check_failover_sa_ctrler_reboot


def _check_failover_switch(mpath_name=None,
                           flag_host=True, flag_physw=False):
    """
    Usage
      _check_failover_switch(mpath_name=>$mpath_name,
          flag_physw=>$flag_physw, flag_host=>$flag_host)
    Purpose
      Check SanMgmt for failover on swtich and physical switch.
    Parameter
      mpath_name     # like "mpatha"
      flag_physw     # physwitch or not
      flag_host      # host level failover or not
    """
    global obj_sanmgmt

    if not mpath_name:
        return None

    port_string = "Storage Array port"
    failover_type_string = "target"
    if flag_host:
        port_string = "HBA port"
        failover_type_string = "host"
        if "iSCSI" in mp.transport_types_of_mpath(mpath_name):
            ports = mp.iface_macs_of_mpath(mpath_name)
        else:
            ports = mp.h_wwpns_of_mpath(mpath_name)
    else:
        ports = mp.t_wwpns_of_mpath(mpath_name)

    switch_string = "switch"
    method_action_up = "link_up"
    method_action_down = "link_down"
    if flag_physw:
        switch_string = "physical switch"
        method_action_up = "phy_port_connect"
        method_action_down = 'phy_port_disconnect'

    if not ports:
        _print("WARN: Multipath %s has no %s " % (mpath_name, failover_type_string)
               + "WWPN")
        _print("WARN: Can't run %s %s level failover on %s" %
               (switch_string, failover_type_string, mpath_name))
        return None

    if len(ports) < 2:
        _print("WARN: Multipath %s only 1 %s " % (mpath_name, failover_type_string)
               + "WWPN")
        _print("WARN: Can't run %s %s level failover on %s" %
               (switch_string, failover_type_string, mpath_name))
        return None

    capability = obj_sanmgmt.capability()
    if not capability:
        _print("FAIL: SanMgmt could not find any capability")
        return None

    if ((method_action_up not in capability) or
            (method_action_down not in capability) or
            not capability[method_action_up] or
            not capability[method_action_down]):
        _print("WARN: SanMgmt cannot do %s/%s on %s" %
               (method_action_up, method_action_down, switch_string))
        print(capability)
        return None

    ready_ports = []
    for port in ports:
        if port not in capability[method_action_down]:
            _print("WARN: SanMgmt cannot do %s on %s port(%s)" %
                   (method_action_down, port_string, port))
            continue
        if port not in capability[method_action_up]:
            _print("WARN: SanMgmt cannot do %s on %s port(%s)" %
                   (method_action_up, port_string, port))
            continue
        ready_ports.append(port)

    if not ready_ports:
        _print("WARN: None of %s Ports can do failover at %s level" %
               (port_string, switch_string))
        return None

    return ready_ports


def check_failover_methods(mpath):
    """
    """
    global opt_failover_mode, all_supported_failover_methods, _check_method_to_func
    if not mpath:
        _print("FAIL: check_failover_methods() - requires mpath parameter")
        return None

    if opt_failover_mode:
        all_failover_methods = re.split(",| ", opt_failover_mode)
        # remove any "empty string that might have been added"
        while "" in all_failover_methods:
            all_failover_methods.remove("")
    else:
        all_failover_methods = all_supported_failover_methods

    failover_method_2_entries = None
    for method in all_failover_methods:
        # Check if mpath supports this failover
        if method in _check_method_to_func:
            failover_entries = _check_method_to_func[method](mpath)
            if failover_entries:
                if not failover_method_2_entries:
                    failover_method_2_entries = {}
                failover_method_2_entries[method] = failover_entries

    return failover_method_2_entries


###############################################################################

def entry_down(entry, failover_method):
    """
    """
    return entry_trigger(entry=entry, failover_method=failover_method, action="DOWN")


def entry_up(entry, failover_method):
    """
    """
    ret = entry_trigger(entry=entry, failover_method=failover_method, action="UP")
    _print("INFO: Waiting 10 seconds for system to detect the revive")
    linux.sleep(10)
    return ret


def entry_trigger(entry=None, failover_method=None, action=None):
    """
    """
    global opt_max_flap_uptime, opt_max_flap_downtime, opt_max_flap_count
    global obj_sanmgmt

    if not entry or not failover_method or not action:
        return False

    if action != "UP" and action != "DOWN":
        _print("FAIL: action %s is not supported by entry_trigger" % action)
        return False

    # _print("DEBUG: Executing %s action %s on %s" % (failover_method, action, entry))

    if failover_method == "sysfs":
        _print("INFO: bringing %s %s via sysfs" % (entry, action))
        return scsi.disk_sys_trigger(entry, action)

    if (failover_method == "fc_host") or (failover_method == "fc_target"):
        _print("INFO: bringing %s %s via %s" % (entry, action, failover_method))
        return obj_sanmgmt.link_trigger(action=action, wwpn=entry)

    if (failover_method == "physw_host") or (failover_method == "physw_target"):
        _print("INFO: bringing %s %s via %s" % (entry, action, failover_method))
        return obj_sanmgmt.phy_link_trigger(action=action, addr=entry)

    if (failover_method == "physw_flap_host") or (failover_method == "physw_flap_target"):
        _print("INFO: Flapping %s via %s" % (entry, failover_method))
        return obj_sanmgmt.phy_link_flap(entry, opt_max_flap_uptime,
                                         opt_max_flap_downtime, opt_max_flap_count)

    if failover_method == "iscsi_host":
        _print("INFO: bringing %s %s via %s" % (entry, action, failover_method))
        return obj_sanmgmt.link_trigger(action=action, addr=entry)

    if failover_method == "iscsi_session":
        _print("INFO: bringing %s %s via %s" % (entry, action, failover_method))
        if action == "UP":
            return iscsi.node_login(entry)
        elif action == "DOWN":
            return iscsi.node_logout(entry)
        else:
            _print("FAIL: unsupported action %s for %s" % (action, failover_method))
            return False

    if failover_method == "sa_ctrler_reboot":
        _print("INFO: bringing controller on port %s %s via %s" % (entry, action, failover_method))
        if action == "UP":
            return obj_sanmgmt.sa_ctrler_wait(entry)
        elif action == "DOWN":
            return obj_sanmgmt.sa_ctrler_reboot(entry)
        else:
            _print("FAIL: unsupported action %s for %s" % (action, failover_method))
            return False

    _print("FAIL: unsupported failover_method %s" % failover_method)
    return False


def _get_scsi_devices_by_entry(mpath, entry):
    """
    Return as list of SCSI devices based on entry
    """
    if not mpath or not entry:
        _print("FAIL: _get_scsi_devices_by_entry() - requires mpath and entry as parameter")
        return None
    if scsi.is_scsi_device(entry):
        return [entry]
    if fc.standardize_wwpn(entry):
        return mp.get_disks_of_mpath_by_wwpn(mpath, entry)
    if net.is_mac(entry):
        return mp.get_disks_of_mpath_by_mac(mpath, entry)
    # For example on iSCSI entry contains target iqn, intercace and portal info:
    _print("WARN: Could not get mpath for entry (%s), returning all SCSI devices from %s" % (entry, mpath))
    return mp.get_disks_of_mpath(mpath)


def execute_failover(mpath=None, failover_method_2_entries=None, flag_quit_on_mp_error=True, dt_pid=None, runtime=None):
    """
    execute_failover ()
    Usage
      execute_failover(mpath=>$mpath_name,
          failover_method_2_entries =failover_method_2_entries,
          dt_pid=dt_pid,
          quit_on_mp_error=>flag_quit_on_mp_error,
          )
    Purpose
      Execute failover in many ways.
    Parameter
      mpath_name             # like "mpathb"
      failover_method_2_entries # return reference of check_failover_methods()
      dt_pid                 # child progress ID which runnig background dt.
      flag_check_mp          # check multipath output or not
      flag_quit_on_mp_error  # quit or not if multipath failed to maintain info
    Returns
      True                       # DT pass and all link failover pass
          or
      False
    """
    global opt_max_interval

    # Test if DT process will finish within its runtime...
    runtime_sec = libsan.misc.time.time_2_sec(runtime)
    runtime_sec += 60  # give 1 minute of tolerance for dt to finish
    expire_time = libsan.misc.time.get_time(in_seconds=True)
    expire_time += runtime_sec

    if not mpath or not failover_method_2_entries:
        _print("FAIL: execute_failover() - requires mpath and failover_method_2_entries parameters")
        return False

    # flag_dt_done = False

    # Run until DT process is over
    flag_dt_done, exit_status = os.waitpid(dt_pid, os.WNOHANG)
    while flag_dt_done == 0:
        for failover_method in failover_method_2_entries:
            # Most of the tests cause some disk from multipath to go down
            # but sa_ctrler_reboot does not as NetApp controller, will fallback
            # To other controller
            # And link flap also does not bring the link down for too long
            expect_disk_down = True
            if (failover_method == "sa_ctrler_reboot" or
                    failover_method == "physw_flap_host" or
                    failover_method == "physw_flap_target"):
                expect_disk_down = False
            _print("\n\nINFO: ==== Executing failover at %s level." % failover_method)

            failover_entries = failover_method_2_entries[failover_method]
            if not failover_entries:
                _print("FAIL: No failover entries available for %s" % failover_method)
                return False

            for entry in failover_entries:
                run("multipath -ll %s" % mpath)

                if dt_pid:
                    flag_dt_done, exit_status = os.waitpid(dt_pid, os.WNOHANG)
                    if flag_dt_done:
                        # DT finished, we can stop failover
                        if exit_status == 0:
                            return True
                        return False
                    # DT did not finish yet, check if it got stuck...
                    if libsan.misc.time.get_time(in_seconds=True) > expire_time:
                        _print("FAIL: DT process should have finished by now, but it did not...")
                        run("ps -ef | grep dt")
                        return False

                pre_running_paths = []
                scsi_disks = mp.get_disks_of_mpath(mpath)
                if not scsi_disks:
                    _print("FAIL: Could not find any SCSI disk for %s" % mpath)
                    return False

                for scsi_disk in scsi_disks:
                    if mp.mpath_check_disk_status(mpath, scsi_disk) == "running":
                        pre_running_paths.append(scsi_disk)
                # running_paths_cmd = "multipathd show paths format '%d, %o, %m' "
                # running_paths_cmd += "| grep -w %s | grep -w running" % mpath
                # ret, output = run(running_paths_cmd, return_output=True)
                # pre_running_paths = len(output.split("\n"))
                # _print("DEBUG: execute_failover() - pre running paths %d" % len(pre_running_paths))

                scsi_devices_port_up = _get_scsi_devices_by_entry(mpath, entry)

                if not scsi_devices_port_up or (len(scsi_devices_port_up) == 0):
                    _print("FAIL: Could not find any SCSI device for: %s" % entry)
                    return False

                _print("\nINFO: Trying to bring %s DOWN via %s" % (entry, failover_method))
                down_ok = entry_down(entry, failover_method)
                if not down_ok:
                    _print("FAIL: Failed to bring %s (%s) DOWN" % (entry, failover_method))
                    entry_up(entry, failover_method)
                    return False
                _print("INFO: Successfully brought %s down via %s" % (entry, failover_method))

                _print("INFO: Interval %d seconds" % opt_max_interval)
                linux.sleep(opt_max_interval)

                run("multipath -ll %s" % mpath)
                sleep_time = 60
                _print("INFO: we wait %ds for the multipathd to get the correct path status" % sleep_time)
                linux.sleep(sleep_time)
                run("multipath -ll %s" % mpath)

                # confirm the multipath detect the disk state change
                # if entry is scsi_device we check it
                # if entry is a WWPN/IQN, we try to find the disks connected to this port
                scsi_devices_port_down = _get_scsi_devices_by_entry(mpath, entry)

                # As the port is down, it is expected to not have any scsi_device connected to it
                # If there is any, they should not be on "running" status
                found_disk_down = False
                if scsi_devices_port_down:
                    for device in scsi_devices_port_down:
                        _print("INFO: Checking status of: %s that is connected to %s" % (device, entry))
                        disk_status = mp.mpath_check_disk_dm_status(mpath, device)
                        # If disk status is None, it is because OS removed the offline device
                        if not disk_status or "active" != disk_status:
                            found_disk_down = True
                        disk_status = mp.mpath_check_disk_path_status(mpath, device)
                        # If disk status is None, it is because OS removed the offline device
                        if not disk_status or "ready" != disk_status:
                            found_disk_down = True

                    # maybe the scsi disk is removed from the path,
                    #  in that case scsi_devices will have less disks than scsi_disks
                    if len(scsi_devices_port_down) < len(scsi_devices_port_up):
                        found_disk_down = True
                else:
                    found_disk_down = True

                if expect_disk_down and not found_disk_down:
                    _print("FAIL: Multipath did not detect disk DOWN")
                    _print("INFO: Restoring %s back up" % entry)
                    entry_up(entry, failover_method)
                    if flag_quit_on_mp_error:
                        return False

                _print("\nINFO: Trying to bring %s UP via %s" % (entry, failover_method))
                up_ok = entry_up(entry, failover_method)
                if not up_ok:
                    _print("FAIL: Failed to bring %s (%s) UP" % (entry, failover_method))
                    return False
                _print("INFO: Successfully brought %s up via %s" % (entry, failover_method))

                run("multipath -ll %s" % mpath)

                _print("INFO: we wait %ds for the multipathd to get the correct path status" % sleep_time)
                linux.sleep(sleep_time)
                run("multipath -ll %s" % mpath)
                # confirm the multipath detect the disk state change
                if scsi.is_scsi_device(entry):
                    scsi_devices = [entry]
                else:
                    if fc.standardize_wwpn(entry):
                        scsi_devices = mp.get_disks_of_mpath_by_wwpn(mpath, entry)
                    else:
                        # For example on iSCSI entry contains target iqn, intercace and portal info:
                        scsi_devices = mp.get_disks_of_mpath(mpath)

                if not scsi_devices:
                    _print("FAIL: Could not get scsi disks UP for %s" % entry)
                    return False

                for device in scsi_devices:
                    disk_status = mp.mpath_check_disk_dm_status(mpath, device)
                    if not disk_status:
                        _print("FAIL: Could not get disk status for %s with %s UP" % (device, entry))
                        _print("INFO: Restoring %s back up" % entry)
                        entry_up(entry, failover_method)
                        if flag_quit_on_mp_error:
                            return False

                    if "active" != disk_status:
                        _print("FAIL: Multipath did not detect disk UP")
                        _print("FAIL: Multipath is reporting the disk with status %s" % disk_status)
                        run("multipath -ll %s" % mpath)
                        _print("INFO: Restoring %s back up" % entry)
                        entry_up(entry, failover_method)
                        if flag_quit_on_mp_error:
                            return False

                post_running_paths = []
                scsi_disks = mp.get_disks_of_mpath(mpath)
                if not scsi_disks:
                    _print("FAIL: Could not find any SCSI disk for %s" % mpath)
                    return False

                for scsi_disk in scsi_disks:
                    if mp.mpath_check_disk_status(mpath, scsi_disk) == "running":
                        post_running_paths.append(scsi_disk)

                # _print("DEBUG: execute_failover() - post running paths %d" % len(post_running_paths))
                if len(pre_running_paths) != len(post_running_paths):
                    _print("FAIL: Different amount of paths after failover")
                    print("Before failover: ", pre_running_paths)
                    print("After failover: ", post_running_paths)
                    return False

        if dt_pid:
            flag_dt_done, exit_status = os.waitpid(dt_pid, os.WNOHANG)
        else:
            # No PID for DT was given, we run just once
            flag_dt_done = 1
        # end while flag_dt_done

    if exit_status == 0:
        return True
    return False


def execute_test(mpath_name):
    global obj_sanmgmt

    mp.multipath_show(mpath_name)

    obj_sanmgmt = sanmgmt.create_sanmgmt_for_mpath(mpath_name)
    if not obj_sanmgmt:
        _print("FAIL: Could not create SanMgmt obj for %s" % mpath_name)
        sys.exit(1)

    # Let get lock for this Storage array
    lock_obj = nfs_lock.setup_nfs_lock_for_mpath(mpath_name)
    if not lock_obj:
        _print("WARN: There is no NFS lock configured!!!")
    lock_type = "exclusive"
    # Tests that do not reboot controller neither change Storage Array port on
    # switch can share the array
    if (opt_failover_mode and (opt_failover_mode == "fc_host"
                               or opt_failover_mode == "physw_flap_host"
                               or opt_failover_mode == "physw_host"
                               or opt_failover_mode == "sysfs"
                               or opt_failover_mode == "iscsi_host"
                               or opt_failover_mode == "iscsi_session")):
        lock_type = "shared"

    # need to request the lock before checking ports, otherwise some port might be down
    # due other server executing tests
    if lock_obj:
        _print("INFO: Requesting NFS lock (%s)..." % lock_type)
        if not lock_obj.request_lock(lock_type):
            _print("FAIL: Could not request NFS lock")
            sys.exit(1)

        _print("INFO: Waiting for NFS lock...")
        if not lock_obj.get_lock():
            _print("FAIL: Give up waiting for lock")
            sys.exit(1)
        _print("INFO: Good, got NFS lock. Start testing...")

    # make sure we have the ports up before querying multipath info
    if not obj_sanmgmt.check_ports_ready():
        _print("FAIL: Not all ports that we need are UP")
        if lock_obj:
            _print("INFO: Releasing for NFS lock...")
            lock_obj.release_lock(lock_type)
        sys.exit(1)

    mpath_info = mp.multipath_query_all(mpath_name)
    if not mpath_info:
        _print("FAIL: Could not get info for mpath: %s" % mpath_name)
        if lock_obj:
            _print("INFO: Releasing for NFS lock...")
            lock_obj.release_lock(lock_type)
        sys.exit(1)

    failover_method_2_entries = check_failover_methods(mpath_name)

    if not failover_method_2_entries:
        _print("SKIP: No failover method available for %s. SKIP this test" % mpath_name)
        if lock_obj:
            _print("INFO: Releasing for NFS lock...")
            lock_obj.release_lock(lock_type)
        sys.exit(2)

    # print mpath_info
    # print failover_method_2_entries
    for failover_method in failover_method_2_entries.keys():
        _print("INFO: %s will perform \"%s\" failover on these entries" % (mpath_name, failover_method))
        for entries in failover_method_2_entries[failover_method]:
            _print("%4s%s" % (" ", entries))

    dt_log_file = "/tmp/dt_stress_mp_failover.log"
    pid = dt.dt_stress_background(of="/dev/mapper/%s" % mpath_name, log=dt_log_file, time=opt_dt_time)
    if not pid:
        _print("FAIL: Could not start DT on background")
        if lock_obj:
            _print("INFO: Releasing for NFS lock...")
            lock_obj.release_lock(lock_type)
        sys.exit(1)

    ok = execute_failover(mpath=mpath_name, failover_method_2_entries=failover_method_2_entries, dt_pid=pid,
                          runtime=opt_dt_time)

    # If for some reason we left some port DOWN, try to bring them UP again
    obj_sanmgmt.check_ports_ready()

    if lock_obj:
        _print("INFO: Releasing for NFS lock...")
        lock_obj.release_lock(lock_type)

    if ok:
        if not log.check_all():
            _print("FAIL: detected error on LogChecker")
            if lock_obj:
                _print("INFO: Releasing for NFS lock...")
                lock_obj.release_lock(lock_type)
            sys.exit(1)

        if lock_obj:
            _print("INFO: Releasing for NFS lock...")
            lock_obj.release_lock(lock_type)
        sys.exit(0)
    else:
        if linux.check_pid(pid):
            _print("FAIL: There was some problem while running execute_failover")
            linux.kill_all("dt")
        else:
            _print("FAIL: Got data corruption when DT I/O stress. Dumping DT log")
            run("cat %s" % dt_log_file)
        if not log.check_all():
            _print("FAIL: detected error on LogChecker")
        if lock_obj:
            _print("INFO: Releasing for NFS lock...")
            lock_obj.release_lock(lock_type)
        sys.exit(1)


def main():
    global opt_failover_mode, opt_max_interval
    global opt_dt_time, opt_max_flap_uptime, opt_max_flap_downtime, opt_max_flap_count

    PASS = 0
    FAIL = 1

    parser = argparse.ArgumentParser(
        description='mp_failover')
    parser.add_argument("--mpath-name", "-m", required=False, dest="mpath_name",
                        help="Name of multipath device to use (We use it to create new device based on it)",
                        metavar="mpath")
    parser.add_argument("--dt-time", required=False, dest="dt_time",
                        default="1h", help="How long should DT run for", metavar="time")
    parser.add_argument("--max-interval", required=False, dest="max_interval",
                        default=1, type=int, help=":")
    parser.add_argument("--quit-on-mp-error", required=False, dest="quit_on_mp_error",
                        help=":")
    parser.add_argument("--max-flap-up-time", required=False, dest="max_flap_uptime",
                        default=100, type=int,
                        help="The max up time in microseconds for physical switch to bring link down when flaping.")
    parser.add_argument("--max-flap-down-time", required=False, dest="max_flap_downtime",
                        default=100, type=int,
                        help="The max down time in microseconds for physical switch to bring link down when flaping.")
    parser.add_argument("--max-flap-count", required=False, dest="max_flap_count",
                        default=50, type=int,
                        help="The max flap count for physical switch to torture the link")
    parser.add_argument("--failover-mode", required=False, dest="failover_mode",
                        help="Specify the only failover mode to run. Current support failover modes:" +
                             "sysfs\n" +
                             "fc_host\n" +
                             "fc_target\n" +
                             "physw_host\n" +
                             "physw_target\n" +
                             "physw_flap_host\n" +
                             "physw_flap_target\n" +
                             "iscsi_session\n" +
                             "sa_ctrler_reboot", metavar="mode_name")

    args = parser.parse_args()

    opt_failover_mode = args.failover_mode
    opt_dt_time = args.dt_time
    opt_max_interval = args.max_interval
    opt_max_flap_uptime = args.max_flap_uptime
    opt_max_flap_downtime = args.max_flap_downtime
    opt_max_flap_count = args.max_flap_count

    mpath_name_list = []
    if args.mpath_name:
        mpath_name_list.append(args.mpath_name)

    # If no mpath was specified search for them on the system
    if not mpath_name_list:
        choosen_devs = sanmgmt.choose_mpaths()
        if not choosen_devs:
            _print("FAIL: Could not find any multipath device to use as base LUN")
            sys.exit(FAIL)
        mpath_name_list = list(choosen_devs.keys())

    error = 0
    for mpath_name in mpath_name_list:
        if not execute_test(mpath_name):
            error += 1

    if error:
        sys.exit(FAIL)
    sys.exit(PASS)


main()
