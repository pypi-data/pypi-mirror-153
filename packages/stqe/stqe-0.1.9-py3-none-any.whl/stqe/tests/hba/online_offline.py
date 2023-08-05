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
import libsan.host.mp as mp
import libsan.host.linux as linux
import libsan.host.dt as dt
import libsan.sanmgmt as sanmgmt
import stqe.host.nfs_lock as nfs_lock
import stqe.host.LogChecker as log
import re
import sys
import subprocess
import argparse
from random import randint

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

    scsi_disks = clean_up_info["scsi_disks"]
    if scsi_disks:
        for scsi_disk in scsi_disks:
            scsi.disk_sys_trigger(scsi_disk, "UP")

    if lock_obj:
        lock_obj.release_lock(LOCK_TYPE)
    _print("INFO: Clean up done.")
    return True


def _check_can_bring_disk_down(scsi_disk):
    """
    Before starting the test, make sure disk can be brought offline
    """
    if not scsi.disk_sys_trigger(scsi_disk, "DOWN"):
        _print("FAIL: Failed to bring disk offline")
        return False
    # make sure we are not able to write to the disk
    ret = run("dd if=/dev/%s of=/dev/null count=1 bs=512 iflag=direct" % scsi_disk)
    if ret == 0:
        _print("FAIL: I/O can still goes to /dev/%s even sysfs marked it as offline"
               % scsi_disk)
        return False
    _print("INFO: Disk is offline as expected")
    if not scsi.disk_sys_trigger(scsi_disk, "UP"):
        _print("FAIL: Failed to bring disk online")
        return False

    return True


def execute_test(mpath_name, rounds, max_interval):
    global LOCK_TYPE, clean_up_info, lock_obj

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
    clean_up_info["scsi_disks"] = scsi_disks

    lock_obj = nfs_lock.setup_nfs_lock_for_mpath(mpath_name)
    if lock_obj:
        _print("INFO: Requesting NFS lock (%s)..." % LOCK_TYPE)
        if not lock_obj.request_lock(LOCK_TYPE):
            _print("FAIL: Could not request NFS lock")
            return False

        _print("INFO: Waiting for NFS lock...")
        if not lock_obj.get_lock():
            _print("FAIL: Give up waiting for lock")
            return False
        _print("INFO: Good, got NFS lock. Start testing...")

    # Just write a bit to make sure there will be an active disk
    if run("dd if=/dev/urandom of=/dev/mapper/%s bs=1k count=256" % mpath_name) != 0:
        mp.multipath_show()
        _print("FAIL: Could not perform IO on %s" % mpath_name)
        return False

    active_disks = mp.mpath_get_active_disk(mpath_name)
    if not active_disks:
        mp.multipath_show()
        _print("FAIL: Could not find any active disk for %s" % mpath_name)
        return False

    for active_disk in active_disks:
        _print("INFO: Testing if it is possible to bring the scsi disk down")
        if not _check_can_bring_disk_down(active_disk):
            _print("FAIL: fail bringing disk %s down" % active_disk)
            return False

    dt.dt_init_data(of="/dev/mapper/%s" % mpath_name)

    _print("INFO: Will trigger sysfs offline/online for these disks of %s" % mpath_name)
    for scsi_disk in scsi_disks:
        print("%8s%s" % (" ", scsi_disk))

    _print("INFO: Bouncing count is %d with max interval of %d" % (rounds, max_interval))
    counter = 0
    while rounds > counter:
        counter += 1
        _print("INFO: Round %d" % counter)
        for scsi_disk in scsi_disks:
            for active_disk in active_disks:
                if not scsi.disk_sys_trigger(scsi_disk, "DOWN"):
                    _print("FAIL: Could not bring disk %s DOWN" % active_disk)
                    return False
            interval = randint(1, max_interval)
            _print("INFO: %s offline interval %d" % (scsi_disk, interval))
            linux.sleep(interval)

            for active_disk in active_disks:
                if not scsi.disk_sys_trigger(scsi_disk, "UP"):
                    _print("FAIL: Could not bring disk %s UP" % active_disk)
                    return False
            interval = randint(1, max_interval)
            _print("INFO: %s online interval %d" % (scsi_disk, interval))
            linux.sleep(interval)

    linux.wait_udev()
    mp.multipath_reload()
    _print("INFO: Bouncing done for %d rounds." % rounds)

    _print("INFO: Verify data on mpath: %s" % mpath_name)
    dt.dt_verify_data("/dev/mapper/%s" % mpath_name)

    _print("INFO: Data verification PASS on %s" % mpath_name)

    _print("INFO: Running I/O stress on %s" % mpath_name)
    if not dt.dt_stress("/dev/mapper/%s" % mpath_name):
        _print("FAIL: DT I/O stress failed on %s" % mpath_name)
        return False

    _print("INFO: Online/Offline test PASS")
    if not log.check_all():
        _print("FAIL: detected error on LogChecker")
        return False

    _print("PASS: Online/Offline test")
    return True


def main():
    """
    """
    PASS = 0
    FAIL = 1

    parser = argparse.ArgumentParser(
        description='add new num')
    parser.add_argument("--mpath-name", "-m", required=False, dest="mpath_name",
                        help="Name of multipath device to use", metavar="mpath")
    parser.add_argument("--rounds", required=False, dest="rounds", default=100,
                        help="How many times the disks will be tests", type=int, metavar="number")
    parser.add_argument("--max-interval", required=False, dest="max_interval", type=int,
                        default=10, help="Maximum time in seconds to wait with disk online/offline", metavar="time")

    args = parser.parse_args()

    mpath_name_list = []
    if args.mpath_name:
        mpath_name_list.append(args.mpath_name)
    rounds = args.rounds
    max_interval = args.max_interval

    # If not mpath was specified search for them on the system
    if not mpath_name_list:
        choosen_devs = sanmgmt.choose_mpaths()
        if not choosen_devs:
            _print("FAIL: Could not find any multipath device to use")
            sys.exit(FAIL)
        mpath_name_list = list(choosen_devs.keys())

    error = 0
    for mpath_name in mpath_name_list:
        if not execute_test(mpath_name, rounds, max_interval):
            error += 1
        _clean_up()

    if error:
        sys.exit(FAIL)
    sys.exit(PASS)


main()
