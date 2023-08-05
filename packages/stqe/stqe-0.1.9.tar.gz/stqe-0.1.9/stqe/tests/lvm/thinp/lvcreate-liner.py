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
    print("INFO: Starting Thinp test")
    print(80 * "#")

    # Create 4 devices
    for dev_num in range(1, 5):
        loop_dev["dev%s" % dev_num] = loopdev.create_loopdev(size=512)
        if not loop_dev["dev%s" % dev_num]:
            TestObj.tfail("Could not create loop device to be used as dev%s" % dev_num)
            return False

    pvs = "%s %s %s %s" % (loop_dev["dev1"], loop_dev["dev2"], loop_dev["dev3"], loop_dev["dev4"])
    if not lvm.vg_create(vg_name, pvs, force=True):
        TestObj.tfail("Could not create VG")
        return False

    # Test thin pool creation with different options
    TestObj.tok("lvcreate -l1 --thin %s/pool1" % vg_name)
    TestObj.tok("lvcreate -l1 -T %s" % vg_name)
    TestObj.tok("lvcreate -l1 -V2G -T %s" % vg_name)
    TestObj.tok("lvcreate -L4M -V2G --thin %s/pool2" % vg_name)
    TestObj.tok("lvcreate -L4M -V2G -T %s/pool3 -n lv1" % vg_name)
    TestObj.tok("lvcreate -L4M -V2G -T %s/pool4 -n %s/lv2" % (vg_name, vg_name))
    TestObj.tok("lvremove -ff %s" % vg_name)

    # Create thin LV in existing pool
    TestObj.tok("lvcreate -L4M -T %s/pool" % vg_name)
    # create thin lv with 2G, lvm will name the LV
    TestObj.tok("lvcreate -V2G -T %s/pool" % vg_name)
    TestObj.tok("lvcreate -V2G -T %s/pool -n lv1" % vg_name)
    TestObj.tok("lvcreate -V2G -T %s/pool -n %s/lv2" % (vg_name, vg_name))
    TestObj.tok("lvremove -ff %s" % vg_name)

    # Test --type thin|thin-pool
    TestObj.tok("lvcreate -l1 --type thin %s/pool1 --virtualsize 1G" % vg_name)
    TestObj.tok("lvcreate -l1 --type thin-pool %s/pool2" % vg_name)
    TestObj.tlog("Test RHEL6.6 --type thin bug 1176006")
    TestObj.tnok("lvcreate -l1 --type thin %s/pool" % vg_name)
    TestObj.tok("lvremove -ff %s" % vg_name)

    # Test --thinpool name/path
    TestObj.tok("lvcreate -l1 -T --thinpool %s/pool3" % vg_name)
    TestObj.tok("lvcreate -l1 --thinpool %s/pool4" % vg_name)
    TestObj.tok("lvcreate -l1 --thinpool pool5 %s" % vg_name)
    TestObj.tok("lvremove -ff %s" % vg_name)

    #
    # Test if LVM lv_metadata_size is correct
    #
    TestObj.tok("lvcreate -L8M -c 256 -T %s/pool1" % vg_name)
    lv_info = lvm.lv_info("pool1", vg_name, options="lv_metadata_size")
    if lv_info["lv_metadata_size"] == "4.00m":
        TestObj.tpass("%s/pool1 lv_metadata_size == 4.00m" % vg_name)
    else:
        TestObj.tfail("%s/pool1 lv_metadata_size == %s, but expected 4.00m" % (vg_name, lv_info["lv_metadata_size"]))

    TestObj.tok("lvcreate -L16M --poolmetadatasize 8 -T %s/pool2" % vg_name)
    lv_info = lvm.lv_info("pool2", vg_name, options="lv_metadata_size")
    if lv_info["lv_metadata_size"] == "8.00m":
        TestObj.tpass("%s/pool2 lv_metadata_size == 8.00m" % vg_name)
    else:
        TestObj.tfail("%s/pool2 lv_metadata_size == %s, but expected 8.00m" % (vg_name, lv_info["lv_metadata_size"]))

    TestObj.tok("lvremove -ff %s" % vg_name)

    #
    # Test --chunksize, -c
    #
    # small chunk size (min is 64KB)
    TestObj.tok("lvcreate --chunksize 64 -l1 -T %s/pool1" % vg_name)
    lv_info = lvm.lv_info("pool1", vg_name, options="chunksize")
    if lv_info["chunksize"] == "64.00k":
        TestObj.tpass("%s/pool1 chunksize == 64.00k" % vg_name)
    else:
        TestObj.tfail("%s/pool1 chunksize == %s, but expected 64.00k" % (vg_name, lv_info["chunksize"]))
    TestObj.tnok("lvcreate -c 32 -l1 -T %s/pool2" % vg_name)

    # big chunk size (max is 1048576 - 1G)
    TestObj.tok("lvcreate --chunksize 1048576 -L1g -T %s/pool2" % vg_name)
    lv_info = lvm.lv_info("pool2", vg_name, options="chunksize")
    if lv_info["chunksize"] == "1.00g":
        TestObj.tpass("%s/pool2 chunksize == 1.00g" % vg_name)
    else:
        TestObj.tfail("%s/pool2 chunksize == %s, but expected 1.00g" % (vg_name, lv_info["chunksize"]))
    TestObj.tnok("lvcreate -c 2097152 -L2g -T %s/pool3" % vg_name)

    # Check if chunk size is correct
    TestObj.tok("lvcreate -l1 -c 512 -T %s/pool3" % vg_name)
    lv_info = lvm.lv_info("pool3", vg_name, options="chunksize")
    if lv_info["chunksize"] == "512.00k":
        TestObj.tpass("%s/pool3 chunksize == 512.00k" % vg_name)
    else:
        TestObj.tfail("%s/pool3 chunksize == %s, but expected 512.00k" % (vg_name, lv_info["chunksize"]))
    TestObj.tok("lvremove -ff %s" % vg_name)

    #
    # Test --extents -l %FREE, VG, PVS
    #
    TestObj.tok("lvcreate --extents 10%%VG -T %s/pool1" % vg_name)
    TestObj.tok("lvcreate -l 10%%PVS -T %s/pool2" % vg_name)
    TestObj.tok("lvcreate -l 10%%PVS -T %s/pool4" % vg_name)
    TestObj.tok("lvcreate -l 10%%FREE -T %s/pool3" % vg_name)
    TestObj.tok("lvcreate -l 100%%FREE -T %s/pool5" % vg_name)
    if not lvm.vg_show():
        TestObj.tfail("Could not show VG %s" % vg_name)
    TestObj.tok("lvremove -ff %s" % vg_name)

    TestObj.tok("lvcreate -l 100%%VG -T %s/pool1" % vg_name)
    TestObj.tok("lvremove -ff %s" % vg_name)
    TestObj.tok("lvcreate -l 100%%PVS -T %s/pool1" % vg_name)
    TestObj.tok("lvremove -ff %s" % vg_name)

    # test with invalid option
    TestObj.tnok("lvcreate --extents 10%%test -T %s/pool1" % vg_name)

    # Since RHEL-6.6 LVM improved usage of percentage allocation
    # lvcreate man page: When expressed as a percentage, the number is  treated
    # as an approximate upper limit for the total number of physical extents to
    # be allocated (including extents used by any mirrors, for example).
    TestObj.tok("lvcreate --extents 110%%FREE -T %s/pool2" % vg_name)
    TestObj.tok("lvremove -ff %s" % vg_name)

    #
    # -virtualsize -V (using different size Unit)
    #
    TestObj.tok("lvcreate -l 90%%FREE -T %s/pool1" % vg_name)
    TestObj.tok("lvcreate -V4096B -T %s/pool1" % vg_name)
    TestObj.tok("lvcreate -V4096K -T %s/pool1" % vg_name)
    TestObj.tok("lvcreate -V4096M -T %s/pool1" % vg_name)
    TestObj.tok("lvcreate -V1G -T %s/pool1" % vg_name)
    TestObj.tok("lvcreate -V1T -T %s/pool1" % vg_name)
    TestObj.tok("lvcreate -V15P -T %s/pool1" % vg_name)
    # Exceed maximum size
    TestObj.tnok("lvcreate -V16P -T %s/pool1" % vg_name)
    TestObj.tok("lvremove -ff %s" % vg_name)

    #
    # --discards
    #
    TestObj.tok("lvcreate -L92m -T %s/pool" % vg_name)
    # default discards is passdown
    lv_info = lvm.lv_info("pool", vg_name, options="discards")
    if lv_info["discards"] == "passdown":
        TestObj.tpass("%s/pool discards == passdown" % vg_name)
    else:
        TestObj.tfail("%s/pool1 discards == %s, but expected passdown" % (vg_name, lv_info["discards"]))

    TestObj.tok("lvcreate -L16m -T %s/pool1 --discards nopassdown" % vg_name)
    lv_info = lvm.lv_info("pool1", vg_name, options="discards")
    if lv_info["discards"] == "nopassdown":
        TestObj.tpass("%s/pool1 discards == nopassdown" % vg_name)
    else:
        TestObj.tfail("%s/pool1 discards == %s, but expected nopassdown" % (vg_name, lv_info["discards"]))

    TestObj.tok("lvcreate -L16m -T %s/pool2 --discards ignore" % vg_name)
    lv_info = lvm.lv_info("pool2", vg_name, options="discards")
    if lv_info["discards"] == "ignore":
        TestObj.tpass("%s/pool2 discards == ignore" % vg_name)
    else:
        TestObj.tfail("%s/pool2 discards == %s, but expected ignore" % (vg_name, lv_info["discards"]))

    TestObj.tok("lvcreate -L16m -T %s/pool3 --discards passdown" % vg_name)
    lv_info = lvm.lv_info("pool3", vg_name, options="discards")
    if lv_info["discards"] == "passdown":
        TestObj.tpass("%s/pool3 discards == passdown" % vg_name)
    else:
        TestObj.tfail("%s/pool3 discards == %s, but expected passdown" % (vg_name, lv_info["discards"]))

    TestObj.tok("lvremove -ff %s" % vg_name)

    #
    # test invalid option
    #
    # Thin pool mirror is not supported
    TestObj.tnok("lvcreate -l1 -m 1 -T %s/pool" % vg_name)

    TestObj.tok("lvcreate -L4M --thin %s/pool" % vg_name)
    TestObj.tnok("lvconvert -m 1 %s/pool" % vg_name)

    TestObj.tok("lvremove -ff %s" % vg_name)

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

    try:
        start_test()
    except Exception as e:
        traceback.print_exc()
        print(e)
        TestObj.tfail("There was some problem while running the test (%s)" % e)

    _clean_up()

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: test pass")
    sys.exit(0)


main()
