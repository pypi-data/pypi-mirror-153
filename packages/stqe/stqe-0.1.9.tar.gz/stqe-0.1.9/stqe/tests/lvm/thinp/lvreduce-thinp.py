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

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import traceback
import stqe.host.tc
import libsan.host.lvm as lvm
import libsan.host.linux as linux
import libsan.host.loopdev as loopdev

from stqe.host.lvm import check_lv_expected_value
from six.moves import range

TestObj = None

loop_dev = {}

vg_name = "testvg"

lv_mnt = "/mnt/lv"
snap_mnt = "/mnt/snap"


def _pool():
    global TestObj, vg_name

    TestObj.tok("lvcreate -L100m -V100m -T %s/pool1 -n lv1" % vg_name)
    TestObj.tok("lvcreate -i2 -L100m -V100m -T %s/pool2 -n lv2" % vg_name)

    TestObj.tnok("lvreduce -l-1 %s/pool1 > /tmp/reduce_pool.err 2>&1" % vg_name)
    TestObj.tok("grep -e 'Thin pool volumes .*cannot be reduced in size yet' /tmp/reduce_pool.err")

    TestObj.tok("lvremove -ff %s" % vg_name)


def _thin_lv():
    global TestObj, vg_name

    TestObj.tok("lvcreate -L100m -V100m -T %s/pool1 -n lv1" % vg_name)
    TestObj.tok("lvcreate -i2 -L100m -V100m -T %s/pool2 -n lv2" % vg_name)

    for lv_num in range(1, 3):
        TestObj.tok("lvreduce -f -l-2 %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name,
                                {"lv_size": "92.00m"})
        # Default unit is m
        TestObj.tok("lvreduce -f -L-8 -n %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_size": "84.00m"})

        TestObj.tok("lvreduce -f -L-8m -n %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_size": "76.00m"})

        # set specific size
        TestObj.tok("lvreduce -f -l18 -n %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_size": "72.00m"})

        TestObj.tok("lvreduce -f -L64m -n %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_size": "64.00m"})

        # Using test option so size will not change
        TestObj.tok("lvreduce -f -l-1%%FREE --test %s/lv%d" % (vg_name, lv_num))
        TestObj.tok("lvreduce -f -l-1%%PVS --test %s/lv%d" % (vg_name, lv_num))
        # Extending thin LV based on VG does not make sense, but leaving this for now
        TestObj.tok("lvreduce -f -l-1%%VG -t %s/lv%d" % (vg_name, lv_num))
        TestObj.tok("lvreduce -f -l-1%%VG -t %s/lv%d" % (vg_name, lv_num))

        if not linux.mkdir(lv_mnt):
            TestObj.tfail("Could not create %s" % lv_mnt)
            return False
        # xfs does not support reduce
        fs = "ext4"

        lv_device = "/dev/mapper/%s-lv%d" % (vg_name, lv_num)
        if not linux.mkfs(lv_device, fs, force=True):
            TestObj.tfail("Could not create fs on %s" % lv_device)
            return False

        if not linux.mount(lv_device, lv_mnt):
            TestObj.tfail("Could not mount %s" % lv_device)
            return False
        TestObj.tok("dd if=/dev/urandom of=%s/lv%d bs=1M count=5" % (lv_mnt, lv_num))

        # reduce FS
        TestObj.tok("yes 2>/dev/null | lvreduce -rf -l-2 %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_size": "56.00m"})

        # snapshot
        snap_device = "/dev/mapper/%s-snap%d" % (vg_name, lv_num)
        TestObj.tok("lvcreate -K -s %s/lv%d -n snap%d" % (vg_name, lv_num, lv_num))
        if not linux.mkdir(snap_mnt):
            TestObj.tfail("Could not create %s" % snap_mnt)
            return False

        if not linux.mkfs(snap_device, fs, force=True):
            TestObj.tfail("Could not create fs on %s" % snap_device)
            return False

        if not linux.mount(snap_device, snap_mnt):
            TestObj.tfail("Could not mount %s" % snap_device)
            return False

        TestObj.tok("dd if=/dev/urandom of=%s/lv%d bs=1M count=5" % (snap_mnt, lv_num))
        # reduce FS
        TestObj.tok("yes 2>/dev/null | lvreduce -l-2 -rf %s/snap%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "snap%d" % lv_num, vg_name, {"lv_size": "48.00m"})
        TestObj.trun("df -h %s" % snap_mnt)

        TestObj.tok("yes 2>/dev/null | lvreduce -L40 -rf %s/snap%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "snap%d" % lv_num, vg_name, {"lv_size": "40.00m"})
        TestObj.trun("df -h %s" % snap_mnt)

        if not linux.umount(lv_mnt):
            TestObj.tfail("Could not umount %s" % lv_device)
            return False
        if not linux.umount(snap_mnt):
            TestObj.tfail("Could not umount %s" % snap_device)
            return False


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting Thin Reduce test")
    print(80 * "#")

    # Create 4 devices
    for dev_num in range(1, 5):
        new_dev = loopdev.create_loopdev(size=256)
        if not new_dev:
            TestObj.tfail("Could not create loop device to be used as dev%s" % dev_num)
            return False
        loop_dev["dev%s" % dev_num] = new_dev

    pvs = ""
    for dev in loop_dev.keys():
        pvs += " %s" % (loop_dev[dev])
    if not lvm.vg_create(vg_name, pvs, force=True):
        TestObj.tfail("Could not create VG")
        return False

    _pool()
    _thin_lv()

    return True


def _clean_up():
    linux.umount(lv_mnt)
    linux.umount(snap_mnt)

    if not lvm.vg_remove(vg_name, force=True):
        TestObj.tfail("Could not delete VG \"%s\"" % vg_name)

    if loop_dev:
        for dev in loop_dev.keys():
            if not lvm.pv_remove(loop_dev[dev]):
                TestObj.tfail("Could not delete PV \"%s\"" % loop_dev[dev])
            linux.sleep(1)
            if not loopdev.delete_loopdev(loop_dev[dev]):
                TestObj.tfail("Could not remove loop device %s" % loop_dev[dev])


def main():
    global TestObj

    TestObj = stqe.host.tc.TestClass()

    linux.install_package("lvm2")

    try:
        start_test()
    except Exception as e:
        traceback.print_exc()
        TestObj.tfail("There was some problem while running the test (%s)" % e)
        print(e)

    _clean_up()

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: test pass")
    sys.exit(0)


main()
