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
import libsan.host.mp as mp
import libsan.host.linux as linux
import libsan.host.fc as fc
import libsan.host.fcoe as fcoe
import libsan.misc.time as time
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
test_tmos = [35, 45, 61]

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

    # TODO: Bring link back up
    if "obj_sanmgmt" in clean_up_info and "h_wwpn" in clean_up_info:
        clean_up_info["obj_sanmgmt"].link_up(clean_up_info["h_wwpn"])
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
        print("FAIL: expected r_port to be with state %s, but it is %s" % (expected_state, r_port_state))
        return False
    return True


def _direct_io_tmo(scsi_disk):
    """
    Perform direct IO to device and return the time it took to fail
    If IO does not fail it returns None
    """
    cmd = "dd if=/dev/%s " % scsi_disk
    cmd += "of=/dev/null count=1 bs=512 iflag=direct"
    io_start_time = time.get_time(in_seconds=True)
    ret, output = run(cmd, return_output=True)
    io_end_time = time.get_time(in_seconds=True)
    if ret == 0:
        # IO did not fail
        return None
    return io_end_time - io_start_time


def dev_loss_tmo_test(mpath_name, tmo, max_link_tmo):
    global clean_up_info, TestObj

    print("INFO: Starting test run for sys/dev_loss_tmo tmo = %s" % tmo)
    if "obj_sanmgmt" not in list(clean_up_info.keys()):
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
    if active_disk not in mp_info["disk"]:
        print("FAIL: Could not find %s on mpath %s" % (active_disk, mpath_name))
        return False
    disk_info = mp_info["disk"][active_disk]

    required_disk_info = ["h_wwpn", "t_wwpn"]
    for req in required_disk_info:
        if req not in disk_info:
            print("FAIL: disk does not provide %s that is required" % req)
            return False
    h_wwpn = disk_info["h_wwpn"]
    t_wwpn = disk_info["t_wwpn"]
    r_port = fc.rport_of_h_wwpn_t_wwpn(h_wwpn=h_wwpn, t_wwpn=t_wwpn)
    if not r_port:
        print("FAIL: Could not find r_port_id")
        return False

    print("INFO:  Choose SCSI disk from mpath: %s" % mpath_name)
    print("\t\tHost WWPN  : %s" % h_wwpn)
    print("\t\tTarget WWPN: %s" % t_wwpn)
    print("\t\tWWID       : %s" % wwid)
    print("\t\tSCSI disk  : %s" % active_disk)
    print("\t\tFC rport   : %s" % r_port)

    # Save h_wwpn to bring it up on clean up
    clean_up_info["h_wwpn"] = h_wwpn
    clean_up_info["r_port"] = r_port

    dev_loss_tmo = fc.get_value_rport_parameter(r_port, "dev_loss_tmo")
    if not dev_loss_tmo:
        print("FAIL: Could not get dev_loss_tmo for %s" % r_port)
        return False
    fast_io_fail_tmo = fc.get_value_rport_parameter(r_port, "fast_io_fail_tmo")
    if not fast_io_fail_tmo:
        print("FAIL: Could not get fast_io_fail_tmo for %s" % r_port)
        return False
    clean_up_info["dev_loss_tmo"] = dev_loss_tmo
    clean_up_info["fast_io_fail_tmo"] = fast_io_fail_tmo
    print("INFO: Original dev_loss_tmo is %s" % dev_loss_tmo)
    print("INFO: Original fast_io_fail_tmo is %s" % fast_io_fail_tmo)

    if not fc.set_value_rport_parameter(r_port, "fast_io_fail_tmo", "off"):
        print("FAIL: Could not set fast_io_fail_tmo of %s to %s" % (r_port, tmo))
        return False
    print("INFO: Active SCSI disk %s(%s) fast_io_fail_tmo is set to 'off'" % (active_disk, r_port))

    if not fc.set_value_rport_parameter(r_port, "dev_loss_tmo", tmo):
        print("FAIL: Could not et dev_loss_tmo of %s to %s" % (r_port, tmo))
        return False
    print("INFO: Active SCSI disk %s(%s) dev_loss_tmo is set to '%s'" % (active_disk, r_port, tmo))

    if not _compare_rport_status(r_port, "Online"):
        return False

    # Bring host port down on switch
    if not obj_sanmgmt.link_down(h_wwpn):
        print("FAIL: Could not bring switch port down")
        return False

    if not _compare_rport_status(r_port, "Blocked"):
        return False

    print("INFO: Checking direct io timeout on failed path")
    io_tmo = _direct_io_tmo(active_disk)
    if io_tmo is None:
        print("FAIL: No I/O error on %s after link failure" % active_disk)
        return False

    if io_tmo > tmo:
        print("FAIL: IO took longer to fail (%ss) than configured (%ss)" % (io_tmo, tmo))
        return False
    print("INFO: I/O successfully failed after %ds" % io_tmo)
    # sleep the remaining timeout
    remaining_time = tmo - io_tmo
    if remaining_time > 0:
        linux.sleep(remaining_time)

    if not _compare_rport_status(r_port, "Not Present"):
        return False

    # Make sure disk device got removed
    linux.wait_udev()
    if os.path.isfile("/dev/%s" % active_disk):
        print("FAIL: SCSI disk should be been removed, but it still exist")
        return False

    # Restore link back up
    if not obj_sanmgmt.link_up(h_wwpn):
        print("FAIL: Could not bring switch port up")
        return False
    # No need to restore port on clean_up
    del clean_up_info["h_wwpn"]

    # Wait port to be restored
    current_port_staus = "Not Present"
    while max_link_tmo > 0:
        print("INFO: Waiting rport came online, timeout: %d" % max_link_tmo)
        linux.sleep(1)
        linux.wait_udev()
        max_link_tmo -= 1
        r_port = fc.rport_of_h_wwpn_t_wwpn(h_wwpn=h_wwpn, t_wwpn=t_wwpn)
        if not r_port:
            # port still not up
            continue
        if not _compare_rport_status(r_port, "Online"):
            # port still not up
            continue
        current_port_staus = "Online"
        new_active_disk = fc.scsi_disk_of_htwwpn_wwid(h_wwpn, t_wwpn, wwid)
        if not new_active_disk:
            continue
        if new_active_disk != active_disk:
            print("INFO: %s got renamed to %s" % (active_disk, new_active_disk))
            active_disk = new_active_disk
        break

    if max_link_tmo == 0 and current_port_staus == "Online":
        print("FAIL: max_link_tmo expired and r_port was not restored")
        return False
    if current_port_staus != "Online":
        # Should not be possible to enter here
        print("FAIL: Did not reach time out, but port still not Online")
        return False

    if _direct_io_tmo(active_disk) is not None:
        print("FAIL: I/O fail, but it should not have to")
        return False
    print("INFO: I/O to %s is restored" % active_disk)
    fc.set_value_rport_parameter(r_port, "fast_io_fail_tmo",
                                 clean_up_info["fast_io_fail_tmo"])
    del clean_up_info["fast_io_fail_tmo"]
    fc.set_value_rport_parameter(r_port, "dev_loss_tmo",

                                 clean_up_info["dev_loss_tmo"])
    del clean_up_info["dev_loss_tmo"]
    mp.mp_start_service()
    linux.sleep(10)
    return True


def execute_test(mpath_name, max_link_tmo):
    global clean_up_info

    obj_sanmgmt = sanmgmt.create_sanmgmt_for_mpath(mpath_name)
    if not obj_sanmgmt:
        _print("FAIL: Got NULL from create_sanmgmt_for_mpath(%s)" % mpath_name)
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

    error = 0
    for tmo in test_tmos:
        if not dev_loss_tmo_test(mpath_name, tmo, max_link_tmo):
            TestObj.tfail("dev_loss_tmo test on %s with timeout %ds" % (mpath_name, tmo))
            break
        print(80 * "#")
        TestObj.tpass("dev_loss_tmo on %s with timeout of %ds" % (mpath_name, tmo))
        print(80 * "#")
    if error:
        return False
    _print("PASS: dev_loss_tmo test")
    return True


def main():
    """
    """
    global TestObj, test_tmos
    PASS = 0
    FAIL = 1

    parser = argparse.ArgumentParser(
        description='dev loss timeout')
    parser.add_argument("--mpath-name", "-m", required=False, dest="mpath_name",
                        help="Name of multipath device to use", metavar="mpath")
    parser.add_argument("--max-link-up-tmo", required=False, dest="max_link_up_tmo", default=20,
                        help="How much time should wait to detect disk", type=int, metavar="number")
    parser.add_argument("--dev-loss-tmo", required=False, dest="dev_loss_tmo", default=None,
                        help="Device loss timeout", type=int, metavar="number")

    args = parser.parse_args()

    TestObj = stqe.host.tc.TestClass()

    mpath_name_list = []
    if args.mpath_name:
        mpath_name_list.append(args.mpath_name)
    if args.dev_loss_tmo:
        test_tmos = [args.dev_loss_tmo]
    max_link_up_tmo = args.max_link_up_tmo

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
            execute_test(mpath_name, max_link_up_tmo)
        except Exception as e:
            print(e)
            TestObj.tfail("Could not execute test on %s" % mpath_name)
            traceback.print_exc()
        _clean_up()

    if not TestObj.tend():
        sys.exit(FAIL)
    sys.exit(PASS)


main()
