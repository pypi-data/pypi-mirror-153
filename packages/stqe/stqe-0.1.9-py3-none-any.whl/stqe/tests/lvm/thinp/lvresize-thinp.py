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


def _extend_pool():
    global TestObj, vg_name

    TestObj.tok("lvcreate -l2 -T %s/pool1" % vg_name)
    TestObj.tok("lvcreate -i2 -l2 -T %s/pool2" % vg_name)

    pvs = []
    for value in loop_dev.values():
        pvs.append(value)

    for pool_num in range(1, 3):
        TestObj.tok("lvresize -l+2 -n %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name,
                                {"lv_size": "16.00m"})
        # Default unit is m
        TestObj.tok("lvresize -L+8 -n %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_size": "24.00m"})
        TestObj.tok("lvresize -L+8M -n %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_size": "32.00m"})

        # Need to use different devices as we are forcing allocation
        if pool_num == 1:
            # extend using some arbitary device
            TestObj.tok("lvresize -l+2 -n %s/pool%d %s" % (vg_name, pool_num, pvs[3]))
            check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_size": "40.00m"})
            # extend using specific range of physical extent
            TestObj.tok("lvresize -l+2 -n %s/pool%d %s:40:41" % (vg_name, pool_num, pvs[2]))
            check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_size": "48.00m"})
            TestObj.tok("pvs -ovg_name,lv_name,devices %s | grep '%s(40)'" % (pvs[2], pvs[2]))

            TestObj.tok("lvresize -l+2 -n %s/pool%d %s:35:37" % (vg_name, pool_num, pvs[1]))
            check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_size": "56.00m"})
            TestObj.tok("pvs -ovg_name,lv_name,devices %s | grep '%s(35)'" % (pvs[1], pvs[1]))

        else:
            # extend using some arbitary device
            TestObj.tok("lvresize -l+2 -n %s/pool%d %s %s" % (vg_name, pool_num, pvs[1], pvs[2]))
            check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_size": "40.00m"})

            TestObj.tok("lvresize -l+2 -n %s/pool%d %s:30-41 %s:20-31" % (vg_name, pool_num, pvs[1], pvs[2]))
            check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_size": "48.00m"})
            TestObj.tok("pvs -ovg_name,lv_name,devices %s | grep '%s(30)'" % (pvs[1], pvs[1]))
            TestObj.tok("pvs -ovg_name,lv_name,devices %s | grep '%s(20)'" % (pvs[2], pvs[2]))

        # set specific size
        TestObj.tok("lvresize -l16 -n %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_size": "64.00m"})
        TestObj.tok("lvresize -L72m -n %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_size": "72.00m"})

        # Using test option so size will not change
        TestObj.tok("lvresize -l+100%%FREE --test %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvresize -l+10%%PVS --test %s/pool%d" % (vg_name, pool_num))
        # Extending thin LV based on VG does not make sense, but leaving this for now
        TestObj.tok("lvresize -l+10%%VG -t %s/pool%d" % (vg_name, pool_num))
        TestObj.tnok("lvresize -l+100%%VG -t %s/pool%d" % (vg_name, pool_num))
    TestObj.tok("lvremove -ff %s" % vg_name)


def _extend_thin_lv():
    global TestObj, vg_name

    TestObj.tok("lvcreate -l10 -V8m -T %s/pool1 -n lv1" % vg_name)
    TestObj.tok("lvcreate -i2 -l10 -V8m -T %s/pool2 -n lv2" % vg_name)

    for lv_num in range(1, 3):
        TestObj.tok("lvextend -l4 %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name,
                                {"lv_size": "16.00m"})
        # Default unit is m
        TestObj.tok("lvextend -L24 -n %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_size": "24.00m"})

        # Using test option so size will not change
        TestObj.tok("lvextend -l+100%%FREE --test %s/lv%d" % (vg_name, lv_num))
        TestObj.tok("lvextend -l+100%%PVS --test %s/lv%d" % (vg_name, lv_num))
        # Extending thin LV based on VG does not make sense, but leaving this for now
        TestObj.tok("lvextend -l+50%%VG -t %s/lv%d" % (vg_name, lv_num))
        TestObj.tok("lvextend -l+120%%VG -t %s/lv%d" % (vg_name, lv_num))

        if not linux.mkdir(lv_mnt):
            TestObj.tfail("Could not create %s" % lv_mnt)
            return False
        fs = linux.get_default_fs()

        lv_device = "/dev/mapper/%s-lv%d" % (vg_name, lv_num)
        if not linux.mkfs(lv_device, fs, force=True):
            TestObj.tfail("Could not create fs on %s" % lv_device)
            return False

        if not linux.mount(lv_device, lv_mnt):
            TestObj.tfail("Could not mount %s" % lv_device)
            return False
        TestObj.tok("dd if=/dev/urandom of=%s/lv%d bs=1M count=5" % (lv_mnt, lv_num))

        # extend FS
        TestObj.tok("lvextend -l+2 -r %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_size": "32.00m"})

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
        # extend FS
        TestObj.tok("lvextend -l+2 -rf %s/snap%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "snap%d" % lv_num, vg_name, {"lv_size": "40.00m"})
        TestObj.trun("df -h %s" % snap_mnt)

        TestObj.tok("lvextend -L48 -rf %s/snap%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "snap%d" % lv_num, vg_name, {"lv_size": "48.00m"})
        TestObj.trun("df -h %s" % snap_mnt)

        if not linux.umount(lv_mnt):
            TestObj.tfail("Could not umount %s" % lv_device)
            return False
        if not linux.umount(snap_mnt):
            TestObj.tfail("Could not umount %s" % snap_device)
            return False
    TestObj.tok("lvremove -ff %s" % vg_name)


###########
# reduce
###########

def _reduce_pool():
    global TestObj, vg_name

    TestObj.tok("lvcreate -L400M -T %s/pool1" % vg_name)
    # reduce thin pool is not supported
    TestObj.tnok("lvresize -l-2 -n %s/pool1" % vg_name)
    check_lv_expected_value(TestObj, "pool1", vg_name, {"lv_size": "400.00m"})

    TestObj.tok("lvremove -ff %s" % vg_name)


def _reduce_thin_lv():
    global TestObj, vg_name

    TestObj.tok("lvcreate -L100m -V100m -T %s/pool1 -n lv1" % vg_name)
    TestObj.tok("lvcreate -i2 -L100m -V100m -T %s/pool2 -n lv2" % vg_name)

    for lv_num in range(1, 3):
        TestObj.tok("lvresize -f -l-2 %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name,
                                {"lv_size": "92.00m"})
        # Default unit is m
        TestObj.tok("lvresize -f -L-8 -n %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_size": "84.00m"})

        TestObj.tok("lvresize -f -L-8m -n %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_size": "76.00m"})

        # set specific size
        TestObj.tok("lvresize -f -l18 -n %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_size": "72.00m"})

        TestObj.tok("lvresize -f -L64m -n %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_size": "64.00m"})

        # Using test option so size will not change
        TestObj.tok("lvresize -f -l-1%%FREE --test %s/lv%d" % (vg_name, lv_num))
        TestObj.tok("lvresize -f -l-1%%PVS --test %s/lv%d" % (vg_name, lv_num))
        # Extending thin LV based on VG does not make sense, but leaving this for now
        TestObj.tok("lvresize -f -l-1%%VG -t %s/lv%d" % (vg_name, lv_num))
        TestObj.tok("lvresize -f -l-1%%VG -t %s/lv%d" % (vg_name, lv_num))

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
        TestObj.tok("yes 2>/dev/null | lvresize -rf -l-2 %s/lv%d" % (vg_name, lv_num))
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
        TestObj.tok("yes 2>/dev/null | lvresize -l-2 -rf %s/snap%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "snap%d" % lv_num, vg_name, {"lv_size": "48.00m"})
        TestObj.trun("df -h %s" % snap_mnt)

        TestObj.tok("yes 2>/dev/null | lvresize -L40 -rf %s/snap%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "snap%d" % lv_num, vg_name, {"lv_size": "40.00m"})
        TestObj.trun("df -h %s" % snap_mnt)

        if not linux.umount(lv_mnt):
            TestObj.tfail("Could not umount %s" % lv_device)
            return False
        if not linux.umount(snap_mnt):
            TestObj.tfail("Could not umount %s" % snap_device)
            return False
    TestObj.tok("lvremove -ff %s" % vg_name)


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting Thin Resize test")
    print(80 * "#")

    linux.install_package("lvm2")

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

    print(80 * "#")
    print("INFO: Starting extend test")
    print(80 * "#")
    _extend_pool()
    _extend_thin_lv()

    print(80 * "#")
    print("INFO: Starting reduce test")
    print(80 * "#")
    _reduce_pool()
    _reduce_thin_lv()

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
