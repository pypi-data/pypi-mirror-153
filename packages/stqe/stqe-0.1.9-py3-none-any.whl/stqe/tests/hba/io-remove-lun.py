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
#   BZ1344381 - multipath: IO does not fail when LUN is deleted on target
#   BZ1181962 - Call trace when running IO on multipath device that fails
#

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
import libsan.host.scsi as scsi
import libsan.host.mp as mp
import libsan.host.linux as linux
import libsan.host.dt as dt
import libsan.misc.time as time
import libsan.sanmgmt as sanmgmt
import stqe.host.nfs_lock as nfs_lock
import stqe.host.LogChecker as log
import re
import sys
import os
import subprocess
import argparse
import traceback

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
    global LOCK_TYPE, clean_up_info

    if not clean_up_info:
        return True

    if clean_up_info["mpath_name"]:
        mp.remove_mpath(clean_up_info["mpath_name"])
        clean_up_info["mpath_name"] = None

    wwid = clean_up_info["wwid"]
    if wwid:
        linux.remove_device_wwid(wwid)
        clean_up_info["wwid"] = None
        _print("INFO: All disks removed from the server")

    obj_sanmgmt = clean_up_info["obj_sanmgmt"]
    lun_name = clean_up_info["lun_name"]
    if lun_name:
        _print("INFO: Deleting %s on the array..." % lun_name)
        if not obj_sanmgmt.lun_remove(lun_name):
            _print("WARN: Could not remove TMP LUN: %s" % lun_name)
        else:
            clean_up_info["lun_name"] = None

    if "lock_obj" in clean_up_info:
        clean_up_info["lock_obj"].release_lock(LOCK_TYPE)
        del clean_up_info["lock_obj"]
    _print("INFO: Cleaned")
    return True


def start_test(mpath_name, lun_size):
    global LOCK_TYPE, clean_up_info, lock_obj

    _print("INFO: Using %s as based multipath device" % mpath_name)
    _print("INFO: Will create new LUN with %s for this test" % lun_size)

    mp_info = mp.multipath_query_all(mpath_name)
    if not mp_info:
        _print("FAIL: Got NULL from query_mp_info(%s)" % mpath_name)
        return False

    obj_sanmgmt = sanmgmt.create_sanmgmt_for_mpath(mpath_name)
    if not obj_sanmgmt:
        _print("FAIL: Got NULL from create_sanmgmt_for_mpath(%s)" % mpath_name)
        return False

    clean_up_info["obj_sanmgmt"] = obj_sanmgmt

    scsi_disks = list(mp_info["disk"].keys())

    scsi_host_ids = []
    for scsi_disk in scsi_disks:
        host_id = scsi.scsi_host_of_scsi_name(scsi_disk)
        if host_id and host_id not in scsi_host_ids:
            scsi_host_ids.append(host_id)

    clean_up_info["lun_name"] = None
    clean_up_info["wwid"] = None
    clean_up_info["mpath_name"] = None

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
            sys.exit(1)
        _print("INFO: Good, got NFS lock. Start testing...")

    lun_base_name = ("io-remove-lun-%s" % time.get_time())
    lun_name = obj_sanmgmt.lun_create_and_map(size=lun_size,
                                              lun_name=lun_base_name, rescan=True)
    if not lun_name:
        _print("FAIL: Could not create LUN for test")
        _clean_up()
        return False
    clean_up_info["lun_name"] = lun_name

    _print("INFO: LUN successfully created")

    if "lun_name" not in clean_up_info:
        _print("FAIL: No LUNs created for test")
        _clean_up()
        return False

    scsi_ids = obj_sanmgmt.scsi_id_of_lun(lun_name=lun_name)
    if not scsi_ids:
        _print("FAIL: Failed to find out the SCSI ID for newly mapped LUN %s" % lun_name)
        run("ls /dev/sd*")
        print(scsi.query_all_scsi_disks())
        _clean_up()
        return False

    _print("INFO: New SCSI disks created:")
    for _ids in scsi_ids:
        _print("    %s - %s" % (_ids, scsi.get_scsi_disk_name(_ids)))

    # All disks should have the same wwid
    scsi_disk = scsi.get_scsi_disk_name(scsi_ids[0])
    wwid = scsi.wwid_of_disk(scsi_disk)
    if not wwid:
        _print("FAIL: Could not find WWID for %s" % scsi_disk)
        _clean_up()
        return False

    clean_up_info["wwid"] = wwid

    _print("INFO: New disks have WWID: %s" % wwid)

    mp.multipath_reload()

    new_mpath = mp.mpath_name_of_wwid(wwid)
    if not new_mpath:
        _print("FAIL: Could not find mpath for WWID %s" % wwid)
        mp.multipath_show()
        _clean_up()
        return False
    clean_up_info["mpath_name"] = new_mpath

    # multipath will try to queue if not path, that might cause it to hang forever
    # so force it to fail if no path
    # as we do not need sector, set it to 0 as man page says

    #    msg = "0 \"fail_if_no_path\""
    #    if not dm.dm_message_dev(new_mpath, msg):
    #        _print("FAIL: Could not disable queue_if_no_path feature")
    #        return False

    _print("INFO: Multipath enabled on tmp LUN: %s" % new_mpath)
    mp.multipath_show()

    new_mp_info = mp.multipath_query_all(new_mpath)
    if not new_mp_info:
        _print("FAIL: Could not query mp info for %s" % new_mpath)
        _clean_up()
        return False

    # Check if the multipath device is configure to queue IO device forever
    # like NetApp
    queue_io = False
    if "queue_if_no_path" in new_mp_info["feature"]:
        queue_io = True

    _print("INFO: LUN successfully found by host")

    pid = dt.dt_stress_background(of="/dev/mapper/%s" % new_mpath,
                                  time="30m", verbose=0)
    if not pid:
        _print("FAIL: Could not start DT I/O stress on %s" % new_mpath)
        _clean_up()
        return False

    linux.sleep(10)
    obj_sanmgmt.lun_remove(lun_name)

    linux.sleep(60)
    mp.multipath_show()

    # need to force IO to fail
    if queue_io:
        linux.kill_all("dt")

    _print("INFO: Waiting for dt to finish...")
    run("ps -ef | grep dt")
    # this case we will block. os.WNOHANG
    flag_dt_done, exit_status = os.waitpid(pid, 0)

    if exit_status == 0:
        _print("FAIL: I/O stress tests passed, it should have failed")
        _clean_up()
        return False

    # Wait to make sure no call trace will happen
    _print("INFO: Wait to make sure there will be no call trace")
    linux.sleep(120)
    _clean_up()
    if not log.check_all():
        _print("FAIL: detected error on LogChecker")
        return False

    _print("PASS: LUN removal with IO test")
    return True


def main():
    """
    """
    PASS = 0
    FAIL = 1

    parser = argparse.ArgumentParser(
        description='add new num')
    parser.add_argument("--mpath-name", "-m", required=False, dest="mpath_name",
                        help="Name of multipath device to use (We use it to create new device based on it)",
                        metavar="mpath")
    parser.add_argument("--lun-size", required=False, dest="lun_size", default="1GiB",
                        help="What size should be the new LUN", metavar="size. Eg: 2GiB")

    args = parser.parse_args()

    mpath_name_list = []
    if args.mpath_name:
        mpath_name_list.append(args.mpath_name)
    lun_size = args.lun_size

    # If not mpath was specified search for them on the system
    if not mpath_name_list:
        choosen_devs = sanmgmt.choose_mpaths()
        if not choosen_devs:
            _print("FAIL: Could not find any multipath device to use as base LUN")
            sys.exit(FAIL)
        mpath_name_list = list(choosen_devs.keys())

    test_pass = False
    try:
        for mpath_name in mpath_name_list:
            test_pass = start_test(mpath_name, lun_size)
    except Exception as e:
        print(e)
        traceback.print_exc()
        e = sys.exc_info()[0]
        _print("FAIL: Exception when running test (%s)" % e)
        _clean_up()
        sys.exit(FAIL)

    if test_pass:
        sys.exit(PASS)

    _clean_up()
    sys.exit(FAIL)


main()
