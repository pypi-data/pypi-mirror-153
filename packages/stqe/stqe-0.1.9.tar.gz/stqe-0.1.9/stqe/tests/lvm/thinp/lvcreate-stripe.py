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
from libsan.host.cmdline import run
import stqe.host.tc
import libsan.host.lvm as lvm
import libsan.host.loopdev as loopdev
import libsan.host.linux as linux
from stqe.host.lvm import check_lv_expected_value
from six.moves import range

TestObj = None

loop_dev = {}

vg_name = "testvg"


def _stripes():
    global TestObj, vg_name

    #
    # -i|--stripes 
    #
    TestObj.tok("lvcreate -i1 -l1 --thin %s/pool1" % vg_name)
    check_lv_expected_value(TestObj, "[pool1_tdata]", vg_name, {"stripes": "1"})

    TestObj.tok("lvcreate --stripes 2 -L4M -V2G -T %s/pool2" % vg_name)
    check_lv_expected_value(TestObj, "[pool2_tdata]", vg_name, {"stripes": "2"})

    TestObj.tok("lvcreate -i3 -L4M -V2G --thin %s/pool3" % vg_name)
    check_lv_expected_value(TestObj, "[pool3_tdata]", vg_name, {"stripes": "3"})

    TestObj.tok("lvcreate --stripes 4 -L4M -V2G -T %s/pool4 -n %s/lv2" % (vg_name, vg_name))
    check_lv_expected_value(TestObj, "[pool4_tdata]", vg_name, {"stripes": "4"})

    # Can not have more stripes than number of devices
    TestObj.tnok("lvcreate --stripes 5 -L4M -V2G -T %s/pool5 -n %s/lv3" % (vg_name, vg_name))

    TestObj.tok("lvremove -ff %s" % vg_name)


def _stripe_size():
    global TestObj, vg_name
    #
    # -I|--stripesize
    #
    # 1 strip will return stripesize == 0
    TestObj.tok("lvcreate -i1 --stripesize 64 -L4M  --thin %s/pool1" % vg_name)
    # stripe size 0 is returned like "0 ". See BZ1391117
    check_lv_expected_value(TestObj, "[pool1_tdata]", vg_name, {"stripes": "1",
                                                                "stripesize": "0 "})

    TestObj.tok("lvcreate -i2 --stripesize 128 -L4M  --thin %s/pool2" % vg_name)
    check_lv_expected_value(TestObj, "[pool2_tdata]", vg_name, {"stripes": "2",
                                                                "stripesize": "128.00k"})

    TestObj.tok("lvcreate -i3 --stripesize 256 -L4M  --thin %s/pool3" % vg_name)
    check_lv_expected_value(TestObj, "[pool3_tdata]", vg_name, {"stripes": "3",
                                                                "stripesize": "256.00k"})
    TestObj.tok("lvremove -ff %s" % vg_name)


def _pool_metadata_size():
    global TestObj, vg_name

    # -- poolmetadatasize
    # default poolmetadatasize is complex to calculate.
    # rounding to the PE size
    TestObj.tok("lvcreate -i1 -L8M -c 256 -T %s/pool1" % vg_name)
    check_lv_expected_value(TestObj, "pool1", vg_name, {"lv_metadata_size": "4.00m"})

    # set poolmetadatasize, default unit is MiB
    TestObj.tok("lvcreate -i2 -L16M --poolmetadatasize 8 -T %s/pool2" % vg_name)
    check_lv_expected_value(TestObj, "pool2", vg_name, {"lv_metadata_size": "8.00m"})

    # Round up to full physical extent
    TestObj.tok("lvcreate -i3 -L16M --poolmetadatasize 2 -T %s/pool3" % vg_name)
    check_lv_expected_value(TestObj, "pool3", vg_name, {"lv_metadata_size": "4.00m"})

    # Too small, minimum is 2MiB
    TestObj.tok("lvcreate -i1 -L16M --poolmetadatasize 1 -T %s/pool4" % vg_name)
    check_lv_expected_value(TestObj, "pool4", vg_name, {"lv_metadata_size": "4.00m"})

    # too big poolmetadatasize (max is 16GB) 
    # test disabled as usually there is not enough space on server to create so big vg
    # TestObj.tok("lvcreate -i3 -L32G --poolmetadatasize 16G -T %s/pool5" % vg_name)
    # check_lv_expected_value("pool5", vg_name, {"lv_metadata_size" : "16.00g"})

    TestObj.tok("lvremove -ff %s" % vg_name)


def _chunk_size():
    global TestObj, vg_name

    # --chunksize, -c, default unit is KiB
    # too small, min is 64KiB
    TestObj.tnok("lvcreate -i2 -c 32 -l1 -T %s/pool1" % vg_name)
    # min size
    TestObj.tok("lvcreate -i1 -c 64 -l1 -T %s/pool1" % vg_name)
    check_lv_expected_value(TestObj, "pool1", vg_name, {"chunksize": "64.00k"})

    # too big, max is 1GiB
    TestObj.tnok("lvcreate -i1 -c 2g -L2g -T %s/pool2" % vg_name)
    # min size
    TestObj.tok("lvcreate -i1 -c 1g -L1g -T %s/pool2" % vg_name)
    check_lv_expected_value(TestObj, "pool2", vg_name, {"chunksize": "1.00g"})

    # set some size
    TestObj.tok("lvcreate -i3 -c 512 -l1 -T %s/pool3" % vg_name)
    check_lv_expected_value(TestObj, "pool3", vg_name, {"chunksize": "512.00k"})
    TestObj.tok("lvremove -ff %s" % vg_name)


def _extents():
    global TestObj, vg_name

    # --extents -l %FREE, VG, PVS
    TestObj.tok("lvcreate -i4 --extents 10%%VG -T %s/pool1" % vg_name)
    TestObj.tok("lvcreate -i2 -l 10%%PVS -T %s/pool2" % vg_name)
    TestObj.tok("lvcreate -i3 -l 10%%VG -T %s/pool3" % vg_name)

    TestObj.tok("lvcreate -i4 -l 10%%FREE -T %s/pool4" % vg_name)
    TestObj.tok("lvcreate -i2 -l 100%%FREE -T %s/pool5" % vg_name)
    run("lvs -a %s" % vg_name)
    TestObj.tok("lvremove -ff %s" % vg_name)
    TestObj.tok("lvcreate -i3 -l 100%%VG -T %s/pool1" % vg_name)
    run("lvs -a %s" % vg_name)
    TestObj.tok("lvremove -ff %s" % vg_name)
    TestObj.tok("lvcreate -i3 -l 100%%PVS -T %s/pool1" % vg_name)
    run("lvs -a %s" % vg_name)
    TestObj.tok("lvremove -ff %s" % vg_name)
    TestObj.tnok("lvcreate -i2 -l 10%%invalid -T %s/pool1" % vg_name)

    # since RHEL-6.6 and 7.1
    # lvcreate man page: When expressed as a percentage,
    # the number is  treated as an approximate upper limit for the total number of physical extents to
    #  be allocated (including extents used by any mirrors, for example).
    # The reason for this is to better fulfill user's request - so he is not blamed there are miising extents.
    TestObj.tok("lvcreate -i3 -l 110%%FREE -T %s/pool1" % vg_name)
    run("lvs -a %s" % vg_name)
    TestObj.tok("lvremove -ff %s" % vg_name)


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting Thin Provisioning Stripe test")
    print(80 * "#")

    # Create 4 devices
    for dev_num in range(1, 5):
        new_dev = loopdev.create_loopdev(size=1280)
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

    _stripes()

    _stripe_size()

    _pool_metadata_size()

    _chunk_size()

    _extents()

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
        TestObj.tfail("There was some problem while running the test (%s)" % e)
        print(e)

    _clean_up()

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: test pass")
    sys.exit(0)


main()
