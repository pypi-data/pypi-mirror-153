#!/usr/bin/python -u
# -u is for unbuffered stdout
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
# Author: Bruno Goncalves   <bgoncalv@redhat.com>

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
import libsan.host.scsi as scsi
import libsan.host.mp as mp
import libsan.host.linux as linux
import libsan.host.dt as dt
import libsan.sanmgmt as sanmgmt
import stqe.host.nfs_lock as nfs_lock
import stqe.host.LogChecker as log
import re
import sys
import os
import subprocess
import argparse
from six.moves import range

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
    global LOCK_TYPE, clean_up_info, lock_obj

    if not clean_up_info:
        return True

    mpath_names = clean_up_info["mpath_names"]
    if mpath_names:
        for mpath in mpath_names:
            mp.remove_mpath(mpath)
        clean_up_info["mpath_names"] = []

    wwids = clean_up_info["wwids"]
    if wwids:
        for wwid in wwids:
            scsi_ids = scsi.scsi_ids_of_wwid(wwid)
            if not scsi_ids:
                continue
            for scsi_id in scsi_ids:
                scsi_disk = scsi.get_scsi_disk_name(scsi_id)
                _print("INFO: Deleting disk: %s" % scsi_disk)
                scsi.delete_disk(scsi_disk)
            mp.mpath_conf_remove('/blacklist_exception/wwid', wwid)
        clean_up_info["wwids"] = []

    _print("INFO: All disks removed from the server")
    obj_sanmgmt = clean_up_info["obj_sanmgmt"]
    lun_names = clean_up_info["lun_names"]
    if lun_names:
        for lun_name in lun_names:
            _print("INFO: Deleting %s on the array..." % lun_name)
            if not obj_sanmgmt.lun_remove(lun_name):
                _print("WARN: Could not remove TMP LUN: %s" % lun_name)
    if lock_obj:
        lock_obj.release_lock(LOCK_TYPE)
    _print("INFO: Cleaned")
    return True


def execute_test(mpath_name, lun_count, lun_size):
    global LOCK_TYPE, clean_up_info, lock_obj

    _print("INFO: Using %s as base device" % mpath_name)
    _print("INFO: Will create %d new LUNs for this test" % lun_count)

    mp_info = mp.multipath_query_all(mpath_name)
    if not mp_info:
        _print("FAIL: Got NULL from query_mp_info(%s)" % mpath_name)
        return False

    obj_sanmgmt = sanmgmt.create_sanmgmt_for_mpath(mpath_name)
    if not obj_sanmgmt:
        _print("FAIL: Got NULL from create_sanmgmt_for_mpath(%s)" % mpath_name)
        return False

    clean_up_info["obj_sanmgmt"] = obj_sanmgmt

    scsi_disks = mp_info["disk"]

    scsi_host_ids = []
    for scsi_disk in scsi_disks:
        host_id = scsi.scsi_host_of_scsi_name(scsi_disk)
        if host_id and host_id not in scsi_host_ids:
            scsi_host_ids.append(host_id)

    clean_up_info["lun_names"] = []
    clean_up_info["wwids"] = []
    clean_up_info["mpath_names"] = []

    lock_obj = nfs_lock.setup_nfs_lock_for_mpath(mpath_name)
    if lock_obj:
        _print("INFO: Requesting NFS lock (%s)..." % LOCK_TYPE)
        if not lock_obj.request_lock(LOCK_TYPE):
            _print("FAIL: Could not request NFS lock")
            return False

        _print("INFO: Waiting for NFS lock...")
        if not lock_obj.get_lock():
            _print("FAIL: Give up waiting for lock")
            sys.exit(1)
        _print("INFO: Good, got NFS lock. Start testing...")

    for lun_cnt in range(1, lun_count + 1):
        lun_name = obj_sanmgmt.lun_create_and_map(size=lun_size)
        if not lun_name:
            _print("FAIL: Could not create LUN %d for add_new_lun test" % lun_cnt)
            _clean_up()
            return False
        clean_up_info["lun_names"].append(lun_name)

    _print("INFO: All LUNs successfully created")

    # need to rescan hosts
    for host in scsi_host_ids:
        scsi.rescan_host(host)
    # if adding more luns we should wait more time
    linux.sleep(6 * lun_count)
    linux.wait_udev()

    if "lun_names" not in clean_up_info:
        _print("FAIL: No LUNs created for test")
        _clean_up()
        return False

    for lun_name in clean_up_info["lun_names"]:
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

        clean_up_info["wwids"].append(wwid)

        _print("INFO: New disks have WWID: %s" % wwid)
        if not mp.mpath_conf_add('/blacklist_exceptions/wwid', wwid):
            _print("FAIL: Cannot enable multipath for WWID: %s" % wwid)
            _clean_up()
            return False

        mp.multipath_reload_conf()
        linux.wait_udev()

        new_mpath = mp.mpath_name_of_wwid(wwid)
        if not new_mpath:
            _print("FAIL: Could not find mpath for WWID %s" % wwid)
            _clean_up()
            return False
        clean_up_info["mpath_names"].append(new_mpath)

        _print("INFO: Multipath enabled on tmp LUN: %s" % new_mpath)

        new_mp_info = mp.multipath_query_all(new_mpath)
        if not new_mp_info:
            _print("FAIL: Could not query mp info for %s" % new_mpath)
            _clean_up()
            return False

        lun_info = obj_sanmgmt.lun_info(lun_name)

        all_scsi_ids_info = scsi.query_all_scsi_disks()
        array_size = int(lun_info["size"])
        for scsi_id in scsi_ids:
            disk_size = int(all_scsi_ids_info[scsi_id]["size"])
            if all_scsi_ids_info[scsi_id]["vendor"] == 'EQLOGIC':
                tolerance = int(array_size * 0.01)
                # check if disk is within tolerance level
                if (disk_size // array_size) < tolerance:
                    array_size = disk_size
            if disk_size != array_size:
                scsi_name = scsi.get_scsi_disk_name(scsi_id)
                _print("FAIL: newly created Disk: %s is holding size: '%s', while on storage array it is: '%s'" % (
                    scsi_name, disk_size, array_size))
                _clean_up()
                return False

        # Check if mpath reported size correctly
        mp_size = new_mp_info["size_bytes"]
        if int(mp_size) != int(lun_info["size"]):
            _print("FAIL: newly created mpath: %s is holding size: %s, while on storage array it is: %s" % (
                new_mpath, mp_size, int(lun_info["size"])))
            _clean_up()
            return False

    # end lun_names for
    _print("INFO: All LUNs successfully found by host")

    # Run DT in all LUNs
    dt_pid_2_info = {}
    for mpath_name in clean_up_info["mpath_names"]:
        dt_log_file = "/tmp/dt_log_%s" % mpath_name
        pid = dt.dt_stress_background(of="/dev/mapper/%s" % mpath_name,
                                      log_file=dt_log_file,
                                      verbose=0)
        if not pid:
            _print("FAIL: Could not start DT I/O stress on %s" % mpath_name)
            _clean_up()
            sys.exit(1)
        dt_pid_2_info[pid] = {"log": dt_log_file,
                              "exit_code": None}

    for dt_pid in dt_pid_2_info.keys():
        # option for non blocking, in this case we will block. os.WNOHANG
        flag_dt_done, exit_status = os.waitpid(dt_pid, 0)
        dt_pid_2_info[dt_pid]["exit_code"] = exit_status

    dt_fail = False
    for dt_pid in dt_pid_2_info.keys():
        if dt_pid_2_info[dt_pid]["exit_code"] != 0:
            _print("FAIL: DT I/O stress PID %s failed with quit code %s" %
                   (dt_pid, dt_pid_2_info[dt_pid]["exit_code"]))
            run("cat %s" % dt_pid_2_info[dt_pid]["log"])
            dt_fail = True

    if not dt_fail:
        _print("INFO: All I/O stress tests PASS")

    _clean_up()
    if not log.check_all() or dt_fail:
        _print("FAIL: detected error on LogChecker or IO error")
        return False

    _print("PASS: All I/O stress tests")
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
    parser.add_argument("--lun-count", required=False, dest="lun_count", default=1,
                        help="How many LUN should be created", type=int, metavar="count")
    parser.add_argument("--lun-size", required=False, dest="lun_size", default="2GiB",
                        help="What size should be the new LUN", metavar="size. Eg: 2GiB")

    args = parser.parse_args()

    mpath_name_list = []
    if args.mpath_name:
        mpath_name_list.append(args.mpath_name)
    lun_count = args.lun_count
    lun_size = args.lun_size

    # If not mpath was specified search for them on the system
    if not mpath_name_list:
        choosen_devs = sanmgmt.choose_mpaths()
        if not choosen_devs:
            _print("FAIL: Could not find any multipath device to use as base LUN")
            sys.exit(FAIL)
        mpath_name_list = list(choosen_devs.keys())

    error = 0
    for mpath_name in mpath_name_list:
        if not execute_test(mpath_name, lun_count, lun_size):
            error += 1

    if error:
        sys.exit(FAIL)
    sys.exit(PASS)


main()
