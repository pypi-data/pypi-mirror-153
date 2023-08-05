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
import stqe.host.tc
import libsan.host.lvm as lvm
import libsan.host.loopdev as loopdev
import libsan.host.linux as linux
from six.moves import range

TestObj = None

loop_dev = {}

vg_name = "testvg"


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting Thinp Metadata Spare")
    print(80 * "#")

    # Create 4 devices
    for dev_num in range(1, 5):
        loop_dev["dev%s" % dev_num] = loopdev.create_loopdev(size=128)
        if not loop_dev["dev%s" % dev_num]:
            TestObj.tfail("Could not create loop device to be used as dev%s" % dev_num)
            return False

    pvs = "%s %s %s %s" % (loop_dev["dev1"], loop_dev["dev2"], loop_dev["dev3"], loop_dev["dev4"])
    if not lvm.vg_create(vg_name, pvs, force=True):
        TestObj.tfail("Could not create VG")
        return False

    # Create pool without spare
    TestObj.tok("lvcreate -l10 --thin %s/pool0 --poolmetadataspare n" % vg_name)
    if not lvm.lv_info("lvol0_pmspare", vg_name):
        TestObj.tpass("lvol0_pmspare does not exist")
    else:
        TestObj.tfail("lvol0_pmspare does exist")

    # will create lvol0_pmspare with size of 4m
    TestObj.tok("lvcreate -l10 --thin %s/pool1 --poolmetadatasize 4m" % vg_name)
    lv_info = lvm.lv_info("[lvol0_pmspare]", vg_name)
    if lv_info and lv_info["size"] == "4.00m":
        TestObj.tpass("%s/lvol0_pmspare lv_size == 4.00m" % vg_name)
    else:
        if not lv_info:
            TestObj.tfail("%s/lvol0_pmspare does not exist" % vg_name)
        else:
            TestObj.tfail("%s/pool1 lv_size == %s, but expected 4.00m" % (vg_name, lv_info["size"]))

    # will change the lvol0_pmspare size to 8m
    TestObj.tok("lvcreate -l10 --thin %s/pool2 --poolmetadatasize 8m" % vg_name)
    lv_info = lvm.lv_info("[lvol0_pmspare]", vg_name)
    if lv_info and lv_info["size"] == "8.00m":
        TestObj.tpass("%s/lvol0_pmspare lvsize == 8.00m" % vg_name)
    else:
        if not lv_info:
            TestObj.tfail("%s/lvol0_pmspare does not exist" % vg_name)
        else:
            TestObj.tfail("%s/pool1 lv_size == %s, but expected 8.00m" % (vg_name, lv_info["size"]))
    TestObj.tok("lvremove -ff %s" % vg_name)

    linux.sleep(5)

    TestObj.tok("lvcreate -l10 --thin %s/pool1 --poolmetadataspare n" % vg_name)
    if not lvm.lv_info("[lvol0_pmspare]", vg_name):
        TestObj.tpass("lvol0_pmspare does not exist")
    else:
        TestObj.tfail("lvol0_pmspare does exist")

    TestObj.tok("lvcreate -l10 --thin %s/pool2 --poolmetadataspare y" % vg_name)
    lv_info = lvm.lv_info("[lvol0_pmspare]", vg_name)
    if lv_info and lv_info["size"] == "4.00m":
        TestObj.tpass("%s/lvol0_pmspare lv_size == 4.00m" % vg_name)
    else:
        if not lv_info:
            TestObj.tfail("%s/lvol0_pmspare does not exist" % vg_name)
        else:
            TestObj.tfail("%s/lvol0_pmspare lv_size == %s, but expected 4.00m" % (vg_name, lv_info["size"]))

    return True


def _clean_up():
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

    start_test()

    _clean_up()

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: test pass")
    sys.exit(0)


main()
