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

#
# Bugs related:
#   BZ1468727 - System crash on rport removal when rport's scsi_target structure is only partialy initialized
#

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
import libsan.host.scsi as scsi
import libsan.host.mp as mp
import libsan.host.linux as linux
import libsan.host.fc as fc
import libsan.host.fcoe as fcoe
import libsan.sanmgmt as sanmgmt
import stqe.host.nfs_lock as nfs_lock
import stqe.host.tc
import re
import sys
import os
import subprocess
import argparse
import traceback

TestObj = None

LOCK_TYPE = "shared"

clean_up_info = {}
lock_obj = None


def _print(string):
    module_name = __name__
    string = re.sub("DEBUG:", "DEBUG:(" + module_name + ") ", string)
    string = re.sub("FAIL:", "FAIL:(" + module_name + ") ", string)
    string = re.sub("FATAL:", "FATAL:(" + module_name + ") ", string)
    string = re.sub("WARN:", "WARN:(" + module_name + ") ", string)

    # Append time information to command
    date = "date \"+%Y-%m-%d %H:%M:%S\""
    p = subprocess.Popen(date, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    stdout = stdout.decode('ascii', 'ignore')
    stdout = stdout.rstrip("\n")

    print("[%s] %s" % (stdout, string))

    sys.stdout.flush()
    if "FATAL:" in string:
        raise RuntimeError(string)
    return


def _clean_up():
    """
    """
    global clean_up_info

    if not clean_up_info:
        return True

    if "rescan_pid" in clean_up_info:
        linux.kill_pid(clean_up_info["rescan_pid"])

    # TODO: Bring link back up
    if ("obj_sanmgmt" in clean_up_info and
            "h_wwpn" in clean_up_info):
        clean_up_info["obj_sanmgmt"].phy_link_trigger(addr=clean_up_info["test_wwpn"],
                                                      action="UP")
        # give some time for r_port to be reconnected
        linux.sleep(10)

    # Restore r_port setting back to original values
    r_port = None
    if "r_port" in clean_up_info:
        r_port = clean_up_info["r_port"]
    if r_port and "fast_io_fail_tmo" in clean_up_info:
        print("INFO: Restoring initial fast_io_fail_tmo value")
        fc.set_value_rport_parameter(r_port, "fast_io_fail_tmo",
                                     clean_up_info["fast_io_fail_tmo"])
    if r_port and "dev_loss_tmo" in clean_up_info:
        print("INFO: Restoring initial dev_loss_tmo value")
        fc.set_value_rport_parameter(r_port, "dev_loss_tmo",
                                     clean_up_info["dev_loss_tmo"])
    mp.mp_start_service()

    if "lock_obj" in clean_up_info:
        clean_up_info["lock_obj"].release_lock(LOCK_TYPE)
    _print("INFO: Clean up done.")
    clean_up_info = {}
    return True


def _compare_rport_status(r_port, expected_state):
    r_port_state = fc.get_value_rport_parameter(r_port, "port_state")
    if not r_port_state:
        print("FAIL: Could not get r_port %s state" % r_port)
        return False
    if r_port_state != expected_state:
        print("FAIL: expected r_port to be with state %s, but it is %s" %
              (expected_state, r_port_state))
        return False
    return True


def dev_loss_tmo_test(mpath_name):
    #    global clean_up_info, TestObj

    print("INFO: Starting test run for sys/oscillate_port dev_loss_tmo = %s" % dev_loss_tmo)
    if "obj_sanmgmt" not in clean_up_info:
        print("FAIL: Could not get obj_sanmgmt")
        return False

    obj_sanmgmt = clean_up_info["obj_sanmgmt"]

    # Force some IO to make sure there is an active path
    run("dd if=/dev/zero of=/dev/mapper/%s count=512" % mpath_name)

    mp_info = mp.multipath_query_all(mpath_name)
    if not mp_info:
        _print("FAIL: Got NULL from query_mp_info(%s)" % mpath_name)
        return False

    mp.multipath_show(mpath_name)
    active_disks = mp.mpath_get_active_disk(mpath_name)
    if not active_disks:
        print("FAIL: Could not find the active path from %s" % mpath_name)
        return False
    # We will test only one of active disks, most common mpath config just have 1 active disk each time anyway
    active_disk = active_disks[0]

    # Stop only after getting the active disk
    print("INFO: Stoping multipathd as it can also control dev_loss_tmo")
    if not mp.mp_stop_service():
        print("FAIL: Could not stop multipath service")
        return False

    clean_up_info["active_disk"] = active_disk

    required_mp_info = ["wwid", "disk"]
    for req in required_mp_info:
        if req not in mp_info:
            print("FAIL: mpath info does not provide %s that is required" % req)
            return False
    wwid = mp_info["wwid"]
    if active_disk not in mp_info["disk"].keys():
        print("FAIL: Could not find %s on mpath %s" % (active_disk, mpath_name))
        return False
    disk_info = mp_info["disk"][active_disk]
    # print "DEBUG: Disk info"
    # print disk_info

    required_disk_info = ["h_wwpn", "t_wwpn"]
    for req in required_disk_info:
        if req not in disk_info.keys():
            print("FAIL: disk does not provide %s that is required" % req)
            return False
    h_wwpn = disk_info["h_wwpn"]
    t_wwpn = disk_info["t_wwpn"]
    host_id = disk_info["host_id"]
    r_port = fc.rport_of_h_wwpn_t_wwpn(h_wwpn=h_wwpn, t_wwpn=t_wwpn)
    if not r_port:
        print("FAIL: Could not find r_port_id")
        return False

    print("INFO:  Choose SCSI disk from mpath: %s" % mpath_name)
    print("\t\tHost ID    : %s" % host_id)
    print("\t\tHost WWPN  : %s" % h_wwpn)
    print("\t\tTarget WWPN: %s" % t_wwpn)
    print("\t\tWWID       : %s" % wwid)
    print("\t\tSCSI disk  : %s" % active_disk)
    print("\t\tFC rport   : %s" % r_port)

    if port_type == "fc_host":
        test_wwpn = h_wwpn
    else:
        test_wwpn = t_wwpn

    if phy_switch:
        if not obj_sanmgmt.get_physw_self(test_wwpn):
            TestObj.tskip("WWPN '%s' is not connected to phy switch" % test_wwpn)
            _clean_up()
            TestObj.tend()
            sys.exit(2)
    else:
        if not obj_sanmgmt.get_sw_self(test_wwpn):
            TestObj.tskip("WWPN '%s' is not connected to SAN switch" % test_wwpn)
            _clean_up()
            TestObj.tend()
            sys.exit(2)

    # Save wwpn to bring it up on clean up
    clean_up_info["test_wwpn"] = test_wwpn

    clean_up_info["r_port"] = r_port

    init_dev_loss_tmo = fc.get_value_rport_parameter(r_port, "dev_loss_tmo")
    if not init_dev_loss_tmo:
        print("FAIL: Could not get dev_loss_tmo for %s" % r_port)
        return False
    init_fast_io_fail_tmo = fc.get_value_rport_parameter(r_port, "fast_io_fail_tmo")
    if not init_fast_io_fail_tmo:
        print("FAIL: Could not get fast_io_fail_tmo for %s" % r_port)
        return False
    clean_up_info["dev_loss_tmo"] = init_dev_loss_tmo
    clean_up_info["fast_io_fail_tmo"] = init_fast_io_fail_tmo
    print("INFO: Original fast_io_fail_tmo is %s" % init_fast_io_fail_tmo)
    print("INFO: Original dev_loss_tmo is %s" % init_dev_loss_tmo)

    if not fc.set_value_rport_parameter(r_port, "fast_io_fail_tmo", "off"):
        print("FAIL: Could not set fast_io_fail_tmo of %s to %s" % (r_port, "off"))
        return False
    print("INFO: Active SCSI disk %s(%s) fast_io_fail_tmo is set to 'off'" %
          (active_disk, r_port))

    if not fc.set_value_rport_parameter(r_port, "dev_loss_tmo", dev_loss_tmo):
        print("FAIL: Could not set dev_loss_tmo of %s to %s" % (r_port, dev_loss_tmo))
        return False
    print("INFO: Active SCSI disk %s(%s) dev_loss_tmo is set to '%s'" %
          (active_disk, r_port, dev_loss_tmo))

    if not _compare_rport_status(r_port, "Online"):
        print("FAIL: r_port %s is already down" % r_port)
        return False

    # Force scsi rescan on background
    # Delete the disks from the server, to force proper rescan of target
    pid = os.fork()
    if pid == 0:
        # I'm child
        while True:
            scsi.rescan_host(host_id, verbose=False)
            targets = fc.get_fc_host_rport_targets(host_id, r_port)
            if not targets:
                continue
            for target in targets:
                devs = fc.get_fc_host_rport_target_devices(host_id, r_port, target)
                if not devs:
                    continue
                for dev in devs:
                    disk = scsi.get_scsi_disk_name(dev)
                    if not disk:
                        continue
                    scsi.delete_disk(disk)
                    # _print("INFO: deleted disk %s" % disk)

    else:
        print("INFO: rescanning host%s on background with PID %s" % (host_id, pid))
        # Bring host port down on switch
        if phy_switch:
            if not obj_sanmgmt.phy_link_oscillate(test_wwpn, min_uptime=min_link_up_tmo,
                                                  max_uptime=max_link_up_tmo,
                                                  min_downtime=min_link_down_tmo,
                                                  max_downtime=max_link_down_tmo,
                                                  count=rounds):
                print("FAIL: To oscillate phy switch port")
                linux.kill_pid(pid)
                return False
        else:
            if not obj_sanmgmt.link_oscillate(test_wwpn, min_uptime=min_link_up_tmo,
                                              max_uptime=max_link_up_tmo,
                                              min_downtime=min_link_down_tmo,
                                              max_downtime=max_link_down_tmo,
                                              count=rounds):
                print("FAIL: To oscillate SAN switch port")
                linux.kill_pid(pid)
                return False
        linux.kill_pid(pid)

    # No need to restore port on clean_up
    del clean_up_info["test_wwpn"]

    current_dev_loss_tmo = fc.get_value_rport_parameter(r_port, "dev_loss_tmo")
    if int(current_dev_loss_tmo) != dev_loss_tmo:
        _print("FAIL: dev_loss_tmo is %s, but expected to be: %s" % (current_dev_loss_tmo, dev_loss_tmo))
        return False

    # Wait port to be restored
    current_port_staus = "Not Present"
    max_wait = 5
    while max_wait > 0:
        print("INFO: Waiting rport came online, timeout: %d" % max_wait)
        linux.sleep(1)
        linux.wait_udev()
        max_wait -= 1
        r_port = fc.rport_of_h_wwpn_t_wwpn(h_wwpn=h_wwpn, t_wwpn=t_wwpn)
        if not r_port:
            # port still not up
            continue
        if not _compare_rport_status(r_port, "Online"):
            # port still not up
            continue
        current_port_staus = "Online"
        break

    if max_wait == 0 and current_port_staus != "Online":
        print("FAIL: max_link_tmo expired and r_port was not restored")
        return False
    if current_port_staus != "Online":
        # Should not be possible to enter here
        print("FAIL: Did not reach time out, but port still not Online")
        return False

    return True


def execute_test(mpath_name):
    obj_sanmgmt = sanmgmt.create_sanmgmt_for_mpath(mpath_name)
    if not obj_sanmgmt:
        TestObj.tfail("Got NULL from create_sanmgmt_for_mpath(%s)" % mpath_name)
        return False

    clean_up_info["obj_sanmgmt"] = obj_sanmgmt

    lock_obj = nfs_lock.setup_nfs_lock_for_mpath(mpath_name)
    if lock_obj:
        clean_up_info["lock_obj"] = lock_obj
        _print("INFO: Requesting NFS lock (%s)..." % LOCK_TYPE)
        if not lock_obj.request_lock(LOCK_TYPE):
            _print("FAIL: Could not request NFS lock")
            return False

        _print("INFO: Waiting for NFS lock...")
        if not lock_obj.get_lock():
            _print("FAIL: Give up waiting for lock")
            return False
        _print("INFO: Good, got NFS lock. Start testing...")

    if not dev_loss_tmo_test(mpath_name):
        TestObj.tfail("oscillate_port test on %s" % mpath_name)
        return False
    _print("PASS: oscillate_port test")
    return True


def main():
    """
    """
    global TestObj, LOCK_TYPE
    global min_link_up_tmo, max_link_up_tmo, min_link_down_tmo, max_link_down_tmo
    global rounds, dev_loss_tmo, port_type, phy_switch
    PASS = 0
    FAIL = 1
    SKIP = 2

    parser = argparse.ArgumentParser(
        description='Test remote port removal when dev_loss happens')
    parser.add_argument("--mpath-name", "-m", required=False, dest="mpath_name",
                        help="Name of multipath device to use", metavar="mpath")
    parser.add_argument("--min-link-up-tmo", required=False, dest="min_link_up_tmo", default=0,
                        help="Minimum amount of time to wait with link up", type=float, metavar="number")
    parser.add_argument("--max-link-up-tmo", required=False, dest="max_link_up_tmo", default=1,
                        help="Maximum amount of time to wait with link up", type=float, metavar="number")
    parser.add_argument("--min-link-down-tmo", required=False, dest="min_link_down_tmo", default=1,
                        help="Minimum amount of time to wait with link up", type=float, metavar="number")
    parser.add_argument("--max-link-down-tmo", required=False, dest="max_link_down_tmo", default=2,
                        help="Maximum amount of time to wait with link up", type=float, metavar="number")
    parser.add_argument("--dev-loss-tmo", required=False, dest="dev_loss_tmo", default=1,
                        help="Device loss timeout", type=int, metavar="number")
    parser.add_argument("--rounds", required=False, dest="rounds", default=500,
                        help="How many times the link should oscillate", type=int, metavar="number")
    parser.add_argument("--port-type", required=True, dest="port_type", default=None,
                        help="Port type", choices=["fc_host", "fc_target"])
    parser.add_argument("--phy-switch", required=False, dest="phy_switch", action="store_true",
                        help="Uses phy switch instead of SAN switch", default=False)

    args = parser.parse_args()

    TestObj = stqe.host.tc.TestClass()

    os_version = linux.dist_ver()
    os_version_minor = linux.dist_ver_minor()

    #Skip running oscialte_port.py on RHEL-7 and RHEL-8 until BZ1527648 is resolved
    if linux.dist_name() == "RHEL":
        #if ((os_version == 8 and os_version_minor < 1) or
                #(os_version == 7 and os_version_minor < 8) or
                #(os_version == 6 and os_version_minor < 11)):
        if ((os_version == 8) or
                (os_version == 7) or
                (os_version == 6)):
            TestObj.tskip("oscillate_port test do not run on %s.%s" % (os_version, os_version_minor))
            TestObj.tend()
            sys.exit(SKIP)

    mpath_name_list = []
    if args.mpath_name:
        mpath_name_list.append(args.mpath_name)
    min_link_up_tmo = args.min_link_up_tmo
    max_link_up_tmo = args.max_link_up_tmo
    min_link_down_tmo = args.min_link_down_tmo
    max_link_down_tmo = args.max_link_down_tmo
    phy_switch = args.phy_switch
    rounds = args.rounds
    dev_loss_tmo = args.dev_loss_tmo
    port_type = args.port_type
    if port_type == "fc_target":
        LOCK_TYPE = "exclusive"

    # If not mpath was specified search for them on the system
    if not mpath_name_list:
        # If no mpath is given, make sure soft fcoe is configured
        # Because test will try to find mpath devices
        fcoe.setup_soft_fcoe()

        choosen_devs = sanmgmt.choose_mpaths()
        if not choosen_devs:
            _print("FAIL: Could not find any multipath device to use")
            sys.exit(FAIL)
        mpath_name_list = list(choosen_devs.keys())

    for mpath_name in mpath_name_list:
        try:
            execute_test(mpath_name)
        except Exception as e:
            print(e)
            TestObj.tfail("Could not execute test on %s" % mpath_name)
            traceback.print_exc()
        _clean_up()

    if not TestObj.tend():
        sys.exit(FAIL)
    sys.exit(PASS)


main()
