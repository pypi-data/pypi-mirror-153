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
#   BZ1404736 - hang on mkfs a 300T Thinp device 
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

lv_mnt = "/mnt/lv"


def _discard():
    global TestObj, vg_name

    TestObj.tok("lvcreate -L1G -V1T -T %s/pool -n discard" % vg_name)

    filesystem = linux.get_default_fs()

    print("INFO: Measuring time of mkfs without discard")
    no_discard_start_time = time.get_time(in_seconds=True)
    TestObj.tok("mkfs.%s -K /dev/mapper/testvg-discard" % filesystem)
    no_discard_end_time = time.get_time(in_seconds=True)

    lvm.lv_show()

    no_discard_time = no_discard_end_time - no_discard_start_time

    TestObj.trun("dd if=/dev/zero of=/dev/mapper/testvg-discard count=1k bs=1k")

    print("INFO: Measuring time of mkfs with discard")
    start_time = time.get_time(in_seconds=True)
    TestObj.tok("mkfs.%s /dev/mapper/testvg-discard" % filesystem)
    end_time = time.get_time(in_seconds=True)

    lvm.lv_show()

    # Make sure the mkfs with discard do not take too much more time than without discard
    max_time = no_discard_time + (no_discard_time * 0.2)
    if end_time < (start_time + max_time):
        TestObj.tpass("discard completed in less than %ss" % max_time)
    else:
        TestObj.tfail("discard completed in more than %ss (%ss)" % (max_time, end_time - start_time))

    TestObj.tok("lvremove -ff %s" % vg_name)


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting Thin Discard Perf test")
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

    _discard()

    return True


def _clean_up():
    #    linux.umount(lv_mnt)

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
        print(e)
        traceback.print_exc()
        e = sys.exc_info()[0]
        TestObj.tfail("There was some problem while running the test (%s)" % e)
        print(e)

    _clean_up()

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: test pass")
    sys.exit(0)


main()
