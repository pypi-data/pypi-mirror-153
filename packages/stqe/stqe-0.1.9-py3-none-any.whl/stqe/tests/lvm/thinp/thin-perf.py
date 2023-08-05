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
#   BZ1405437 - Performance degradation on thin logical volumes
#

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import traceback
import stqe.host.tc
import libsan.host.lvm as lvm
import libsan.host.linux as linux
import libsan.host.loopdev as loopdev
import libsan.misc.time as time
from six.moves import range

TestObj = None

loop_dev = {}

vg_name = "testvg"

thin_lv_mnt = "/mnt/thin_lv"
regular_lv_mnt = "/mnt/regular_lv"


def _thin_lv():
    global TestObj, vg_name

    TestObj.tok("lvcreate -L1G -V 900M -T %s/pool -n thin_lv" % vg_name)
    TestObj.tok("lvcreate -L900M -n regular_lv %s" % vg_name)

    filesystem = linux.get_default_fs()

    regular_lv_dev = "/dev/mapper/testvg-regular_lv"
    thin_lv_dev = "/dev/mapper/testvg-thin_lv"

    if not linux.mkfs(thin_lv_dev, filesystem, force=True):
        TestObj.tfail("Could not create FS on %s" % thin_lv_dev)
        return

    if not linux.mkfs(regular_lv_dev, filesystem, force=True):
        TestObj.tfail("Could not create FS on %s" % regular_lv_dev)
        return

    linux.mkdir(thin_lv_mnt)
    linux.mkdir(regular_lv_mnt)

    if not linux.mount(regular_lv_dev, regular_lv_mnt):
        TestObj.tfail("Could not mount %s" % regular_lv_dev)
        return

    if not linux.mount(thin_lv_dev, thin_lv_mnt):
        TestObj.tfail("Could not mount %s" % thin_lv_dev)
        return

    # Create a file
    TestObj.trun("dd if=/dev/urandom of=/tmp/test.img count=200k bs=4k")

    # Time for WRITE
    print("INFO: Measuring time of write on regular LV")
    regular_lv_start_time = time.get_time(in_seconds=True)
    for i in range(1, 5):
        TestObj.tok("cp /tmp/test.img %s; sync" % regular_lv_mnt)
    #       TestObj.tok("rm -f %s/*; sync" % regular_lv_mnt)
    regular_lv_end_time = time.get_time(in_seconds=True)

    regular_lv_time = regular_lv_end_time - regular_lv_start_time

    print("INFO: Measuring time of write on thin LV")
    thin_lv_start_time = time.get_time(in_seconds=True)
    for i in range(1, 5):
        TestObj.tok("cp /tmp/test.img %s; sync" % thin_lv_mnt)
    #        TestObj.tok("rm -f %s/*; sync" % thin_lv_mnt)
    thin_lv_end_time = time.get_time(in_seconds=True)

    # Make sure the mkfs with discard do not take too much more time than without discard
    max_time = regular_lv_time + (int(round(regular_lv_time * 0.1)))
    if thin_lv_end_time <= (thin_lv_start_time + max_time):
        TestObj.tpass("write on thin lv completed in less than %ss" % max_time)
    else:
        TestObj.tfail(
            "write on thin lv completed in more than %ss (%ss)" % (max_time, thin_lv_end_time - thin_lv_start_time))

    # Time for READ
    print("INFO: Measuring time of read on regular LV")
    regular_lv_start_time = time.get_time(in_seconds=True)
    for i in range(1, 5):
        TestObj.tok("cp %s/test.img /tmp/test_regular.img; sync" % regular_lv_mnt)
    #        TestObj.tok("rm -f /tmp/test_regular.img; sync")
    regular_lv_end_time = time.get_time(in_seconds=True)

    regular_lv_time = regular_lv_end_time - regular_lv_start_time

    print("INFO: Measuring time of read on thin LV")
    thin_lv_start_time = time.get_time(in_seconds=True)
    for i in range(1, 5):
        TestObj.tok("cp %s/test.img /tmp/test_thin.img; sync" % thin_lv_mnt)
    #        TestObj.tok("rm -f /tmp/test_thin.img; sync")
    thin_lv_end_time = time.get_time(in_seconds=True)

    lvm.lv_show()

    # Make sure the mkfs with discard do not take too much more time than without discard
    max_time = regular_lv_time + (int(round(regular_lv_time * 0.1)))
    if thin_lv_end_time <= (thin_lv_start_time + max_time):
        TestObj.tpass("read on thin lv completed in less than %ss" % max_time)
    else:
        TestObj.tfail(
            "read on thin lv completed in more than %ss (%ss)" % (max_time, thin_lv_end_time - thin_lv_start_time))


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting Thin LV Perf test")
    print(80 * "#")

    # Create 1 device
    for dev_num in range(1, 5):
        new_dev = loopdev.create_loopdev(size=800)
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

    _thin_lv()

    return True


def _clean_up():
    linux.umount(thin_lv_mnt)
    linux.umount(regular_lv_mnt)

    TestObj.trun("rm -f /tmp/test*.img")

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
        _clean_up()
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
