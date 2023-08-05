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
#
# Author: Bruno Goncalves   <bgoncalv@redhat.com>

#
# Bugs related:
#   BZ1305983 - thin pool with error target meta device causes kernel panic 
#
from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.loopdev import create_loopdev, delete_loopdev
from libsan.host.dm import dm_set_target_type
from libsan.host.cmdline import run
from libsan.host.lvm import vg_create, vg_remove, pv_remove
from libsan.host.linux import sleep, install_package
import stqe.host.tc
import sys

TestObj = None

loop_dev = None

vg_name = "VG"
pool_name = "POOL"


def main():
    global TestObj

    install_package("lvm2")

    start_test()

    _clean_up()

    print("INFO: waiting 5 mins to make sure system did not crash after removing test VG")
    sleep(5 * 60)

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: Test pass")
    sys.exit(0)


def start_test():
    global TestObj

    TestObj = stqe.host.tc.TestClass()

    _clean_up()

    # create loop device of 10G
    global loop_dev
    loop_dev = create_loopdev("loop0", 10 * 1024)
    if not loop_dev:
        TestObj.tfail("Could not create loop device")
        return False

    if not vg_create(vg_name, loop_dev):
        TestObj.tfail("Could not create VG \"%s\"" % vg_name)
        return False

    print("INFO: Creating LVs")
    TestObj.tok("lvcreate --thinpool %s --zero n -L 5G --poolmetadatasize 4M %s"
                % (pool_name, vg_name))
    TestObj.tok("lvcreate --virtualsize 1G -T %s/%s -n origin" % (vg_name, pool_name))
    TestObj.tok("lvcreate --virtualsize 1G -T %s/%s -n other1" % (vg_name, pool_name))
    TestObj.tok("lvcreate -k n -s /dev/%s/origin -n snap1" % vg_name)

    print("INFO: Displaying LVs")
    TestObj.tok("lvs -a -o +devices")
    # going to metadata LV to error
    dm_dev = "%s-%s_tmeta" % (vg_name, pool_name)

    run("dmsetup table | grep tmeta")

    print("INFO:Going to set %s to error" % dm_dev)
    if not dm_set_target_type("%s" % dm_dev, "error"):
        TestObj.tfail("Could not set metadata LV to error")
        return False

    # list the devices again
    print("INFO: Going to display the devices now, it might to show some error")
    TestObj.tok("lvs -a -o +devices")

    run("dmsetup table | grep tmeta")

    print("INFO: rescaning for PV")
    TestObj.tok("pvscan")

    print("INFO: waiting 5 mins to make sure system did not crash")
    # BZ1305983 fails at this point
    sleep(5 * 60)

    return True


def _clean_up():
    global vg_name, loop_dev

    # make sure any failed device is removed
    run("dmsetup remove_all")
    if not vg_remove(vg_name, force=True):
        TestObj.tfail("Could not delete VG \"%s\"" % vg_name)

    if loop_dev:
        if not pv_remove(loop_dev):
            TestObj.tfail("Could not delete PV \"%s\"" % loop_dev)
        delete_loopdev(loop_dev)


main()
