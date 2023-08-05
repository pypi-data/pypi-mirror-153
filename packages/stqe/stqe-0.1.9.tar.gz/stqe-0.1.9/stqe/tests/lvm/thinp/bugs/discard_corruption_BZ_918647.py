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
#

from __future__ import absolute_import, division, print_function, unicode_literals
import traceback
import sys
import stqe.host.tc
from libsan.host.loopdev import create_loopdev, delete_loopdev
import libsan.host.lvm as lvm
import libsan.host.linux as linux

TestObj = None

loop_dev = None

vg_name = "VG"
pool_name = "POOL"
origin_mnt = "/tmp/origin_mnt"
snap_mnt = "/tmp/snap_mnt"


def main():
    global TestObj

    linux.install_package("lvm2")

    try:
        start_test()
    except Exception as e:
        print(e)
        traceback.print_exc()
        e = sys.exc_info()[0]
        TestObj.tfail("There was some problem while running the test (%s)" % e)
        print(e)

    _clean_up()

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: Test pass")
    sys.exit(0)


def start_test():
    global TestObj

    TestObj = stqe.host.tc.TestClass()
    TestObj.trun("rpm -q lvm2")

    _clean_up()

    global loop_dev
    loop_dev = create_loopdev("loop0", 512)
    if not loop_dev:
        TestObj.tfail("Could not create loop device")
        return False

    if not lvm.vg_create(vg_name, loop_dev):
        TestObj.tfail("Could not create VG \"%s\"" % vg_name)
        return False

    print("INFO: Creating LV")
    TestObj.tok("lvcreate -V100m -l125 -T %s/%s -n origin"
                % (vg_name, pool_name))
    TestObj.tok("lvchange --discards nopassdown %s/%s" % (vg_name, pool_name))
    if not linux.mkfs("/dev/%s/origin" % vg_name, "ext4"):
        TestObj.tfail("Could not create FS for origin")
        return False
    if not linux.mkdir(origin_mnt):
        TestObj.tfail("Could not create mnt directory to origin")
        return False
    if not TestObj.tok("mount /dev/%s/origin %s" % (vg_name, origin_mnt)):
        return False

    # Create a file
    if not TestObj.tok("sync; dd if=/dev/zero of=%s/file1 bs=1M count=60; sync" % origin_mnt):
        return False

    print("INFO: Creating snapshot")
    # create the snapshot
    if not TestObj.tok("lvcreate -K -s %s/origin -n %s/snap1" % (vg_name, vg_name)):
        return False
    linux.sleep(5)

    # Show VG discard info
    TestObj.trun("lvs %s -o+discards" % vg_name)
    pool_info = lvm.lv_info(pool_name, vg_name, "data_percent")
    origin_info = lvm.lv_info("origin", vg_name, "data_percent")
    snap_info = lvm.lv_info("snap1", vg_name, "data_percent")
    pre_dp_pool = float(pool_info["data_percent"])
    pre_dp_origin = float(origin_info["data_percent"])
    pre_dp_snap = float(snap_info["data_percent"])

    # rm files on the origin and do discard
    TestObj.tok("rm -rf %s/file1;sync" % origin_mnt)
    TestObj.tok("fstrim -vvv %s;sync" % origin_mnt)
    TestObj.trun("umount %s" % origin_mnt)
    linux.sleep(5)

    print("INFO: Checking if data percentage got reduced only on origin")
    TestObj.trun("lvs %s -o+discards" % vg_name)
    pool_info = lvm.lv_info(pool_name, vg_name, "data_percent")
    origin_info = lvm.lv_info("origin", vg_name, "data_percent")
    snap_info = lvm.lv_info("snap1", vg_name, "data_percent")
    now_dp_pool = float(pool_info["data_percent"])
    now_dp_origin = float(origin_info["data_percent"])
    now_dp_snap = float(snap_info["data_percent"])

    pool_diff = pre_dp_pool / now_dp_pool

    # the pool's data percentage is a little different from the previous one (2% tolerance)
    if pool_diff > 1.02 or pool_diff < 0.98:
        TestObj.tfail("Data pool different is too big: %s" % pool_diff)
        print("FAIL: pre_dp_pool: %s - now_dp_pool: %s - diff: %s" % (pre_dp_pool, now_dp_pool, pool_diff))
        return False

    # the data percentage of snapshot, it should keep the same
    if now_dp_snap != pre_dp_snap:
        TestObj.tfail("data percentage of snap should not have changed")
        print("FAIL: pre_dp_snap: %s - now_dp_snap: %s" % (pre_dp_snap, now_dp_snap))
        return False

    # the data percentage of origin, it should reduce
    if now_dp_origin >= pre_dp_origin:
        TestObj.tfail("data percentage of origin should have reduced")
        print("FAIL: pre_dp_origin: %s - now_dp_origin: %s" % (pre_dp_origin, now_dp_origin))
        return False

    #
    # do discards on the snap1
    #
    print("INFO: Deleting data from snapshot")
    if not linux.mkdir(snap_mnt):
        TestObj.tfail("Could not create mnt directory to snap")
        return False
    if not TestObj.tok("mount /dev/%s/snap1 %s" % (vg_name, snap_mnt)):
        return False
    TestObj.tok("rm -rf %s/file1;sync" % snap_mnt)
    TestObj.tok("fstrim -vvv %s;sync" % snap_mnt)
    linux.sleep(5)

    print("INFO: Checking if data percentage got reduced on snapshot and pool")
    TestObj.trun("lvs %s -o+discards" % vg_name)
    pool_info = lvm.lv_info(pool_name, vg_name, "data_percent")
    origin_info = lvm.lv_info("origin", vg_name, "data_percent")
    snap_info = lvm.lv_info("snap1", vg_name, "data_percent")
    post_dp_pool = float(pool_info["data_percent"])
    post_dp_origin = float(origin_info["data_percent"])
    post_dp_snap = float(snap_info["data_percent"])

    # the pool's data percentage should be reduced
    if post_dp_pool >= now_dp_pool:
        TestObj.tfail("Data pool percentage did not reduce")
        print("FAIL: post_dp_pool: %s - now_dp_pool: %s" % (post_dp_pool, now_dp_pool))
        return False

    # the data percentage of snapshot should be reduced
    if post_dp_snap >= now_dp_snap:
        TestObj.tfail("data percentage of snap should have changed")
        print("FAIL: post_dp_snap: %s - now_dp_snap: %s" % (post_dp_snap, now_dp_snap))
        return False

    # the data percentage of origin, it should keep the same
    if post_dp_origin != now_dp_origin:
        TestObj.tfail("data percentage of origin should not have changed")
        print("FAIL: post_dp_origin: %s - now_dp_origin: %s" % (post_dp_origin, now_dp_origin))
        return False

    TestObj.trun("umount %s" % snap_mnt)

    return True


def _clean_up():
    global vg_name, loop_dev

    TestObj.trun("umount %s" % origin_mnt)
    TestObj.trun("umount %s" % snap_mnt)

    if not lvm.vg_remove(vg_name, force=True):
        TestObj.tfail("Could not delete VG \"%s\"" % vg_name)

    if loop_dev:
        if not lvm.pv_remove(loop_dev):
            TestObj.tfail("Could not delete PV \"%s\"" % loop_dev)
        delete_loopdev(loop_dev)


main()
