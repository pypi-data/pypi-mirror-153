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
from stqe.host.lvm import check_lv_expected_value
from six.moves import range

TestObj = None

loop_dev = {}

vg_name = "testvg"


def _pool_test():
    global TestObj, vg_name

    # Test on 2 pools
    for pool_num in range(1, 3):
        # testing change discards with active pool and active thin volume
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"discards": "passdown"})

        # Change passdown <-> ignore should not work
        TestObj.tnok("lvchange --discards ignore %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"discards": "passdown"})

        # Change passdown <-> nopassdown is supported
        TestObj.tok("lvchange --discards nopassdown %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"discards": "nopassdown"})

        # Change nopassdown <-> ignore should not work
        TestObj.tnok("lvchange --discards ignore %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"discards": "nopassdown"})

        TestObj.tok("lvchange --discards passdown %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"discards": "passdown"})

        # For RHEL, since RHEL-6.7 the LVM attribute when is active should be twi-aotz--, before was twi-a-tz--
        expected_online_attr = "twi-aotz--"

        # testing change discards with inactive pool and inactive thin volume
        # Change passdown <-> ignore is supported
        TestObj.tok("lvchange -an %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvchange -an %s/lv%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name,
                                {"discards": "passdown", "lv_attr": "twi---tz--"})
        TestObj.tok("lvchange --discards ignore %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvchange -ay %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvchange -ay %s/lv%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name,
                                {"discards": "ignore", "lv_attr": expected_online_attr})

        # Change ignore <-> nopassdown is supported
        TestObj.tok("lvchange -an %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvchange -an %s/lv%d" % (vg_name, pool_num))
        TestObj.tok("lvchange --discards nopassdown %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvchange -ay %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvchange -ay %s/lv%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"discards": "nopassdown"})

        TestObj.tok("lvchange -an %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvchange -an %s/lv%d" % (vg_name, pool_num))
        TestObj.tok("lvchange --discards ignore %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvchange -ay %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvchange -ay %s/lv%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"discards": "ignore"})

        # Change passdown <-> ignore is supported
        TestObj.tok("lvchange -an %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvchange -an %s/lv%d" % (vg_name, pool_num))
        TestObj.tok("lvchange --discards passdown %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvchange -ay %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvchange -ay %s/lv%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"discards": "passdown"})

        # It is not possible to change thin pool to readonly
        err_msg = "Command not permitted on LV"
        if linux.dist_name() == "RHEL" and linux.dist_release() < "7.4":
            err_msg = "not yet supported"
        TestObj.tok("lvchange -p r %s/pool%d 2>&1 | grep '%s'" % (vg_name, pool_num, err_msg))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_attr": expected_online_attr})

        # refresh
        TestObj.tok("lvchange --refresh %s/pool%d" % (vg_name, pool_num))

        # monitor
        TestObj.tok("lvchange --monitor n %s/pool%d" % (vg_name, pool_num))
        TestObj.tok("lvchange --monitor y %s/pool%d" % (vg_name, pool_num))

        # allocation policy
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_allocation_policy": "inherit"})
        TestObj.tok("lvchange -Cy %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_allocation_policy": "contiguous"})
        TestObj.tok("lvchange -Cn %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_allocation_policy": "inherit"})

        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_read_ahead": "auto"})

        # set read ahead to use 256 sectors
        TestObj.tok("lvchange -r 256 %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_read_ahead": "128.00k"})
        TestObj.tok("lvchange -r none %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_read_ahead": "0 "})
        TestObj.tok("lvchange -r auto %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"lv_read_ahead": "auto"})

        # if zeroing is enabled
        TestObj.tok("lvchange -Zn %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"zero": ""})
        TestObj.tok("lvchange -Z y %s/pool%d" % (vg_name, pool_num))
        check_lv_expected_value(TestObj, "pool%d" % pool_num, vg_name, {"zero": "zero"})


def _lv_test():
    # Test the 2 LVs

    for lv_num in range(1, 3):
        TestObj.tok("lvchange -an %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_attr": "Vwi---tz--"})
        TestObj.tnok("ls /dev/%s/lv%d" % (vg_name, lv_num))
        TestObj.tok("lvchange -a y %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_attr": "Vwi-a-tz--"})
        TestObj.tok("ls /dev/%s/lv%d" % (vg_name, lv_num))

        # change to readonly and back to rw
        TestObj.tok("lvchange -pr %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_attr": "Vri-a-tz--"})
        TestObj.tok("lvchange -p rw %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_attr": "Vwi-a-tz--"})

        TestObj.tok("lvchange --refresh %s/lv%d" % (vg_name, lv_num))

        # allocation policy
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_allocation_policy": "inherit"})
        TestObj.tok("lvchange -Cy %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_allocation_policy": "contiguous"})
        TestObj.tok("lvchange -Cn %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_allocation_policy": "inherit"})

        # set read ahead to use 256 sectors
        TestObj.tok("lvchange -r 256 %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_read_ahead": "128.00k"})
        TestObj.tok("lvchange -r none %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_read_ahead": "0 "})
        TestObj.tok("lvchange -r auto %s/lv%d" % (vg_name, lv_num))
        check_lv_expected_value(TestObj, "lv%d" % lv_num, vg_name, {"lv_read_ahead": "auto"})


def _snapshot_test():
    TestObj.tok("lvcreate -s %s/lv1 -n lv3" % vg_name)
    # snapshot is not active when created
    check_lv_expected_value(TestObj, "lv3", vg_name, {"lv_attr": "Vwi---tz-k"})
    TestObj.tnok("ls /dev/%s/lv3" % vg_name)
    # must use -K to active snapshot
    TestObj.tok("lvchange -ay -K %s/lv3" % vg_name)
    check_lv_expected_value(TestObj, "lv3", vg_name, {"lv_attr": "Vwi-a-tz-k"})
    TestObj.tok("ls /dev/%s/lv3" % vg_name)

    TestObj.tok("lvchange -pr %s/lv3" % vg_name)
    check_lv_expected_value(TestObj, "lv3", vg_name, {"lv_attr": "Vri-a-tz-k"})
    TestObj.tok("lvchange -p rw %s/lv3" % vg_name)
    check_lv_expected_value(TestObj, "lv3", vg_name, {"lv_attr": "Vwi-a-tz-k"})

    TestObj.tok("lvchange --refresh %s/lv3" % vg_name)

    # allocation policy
    check_lv_expected_value(TestObj, "lv3", vg_name, {"lv_allocation_policy": "inherit"})
    TestObj.tok("lvchange -Cy %s/lv3" % vg_name)
    check_lv_expected_value(TestObj, "lv3", vg_name, {"lv_allocation_policy": "contiguous"})
    TestObj.tok("lvchange -Cn %s/lv3" % vg_name)
    check_lv_expected_value(TestObj, "lv3", vg_name, {"lv_allocation_policy": "inherit"})

    # set read ahead to use 256 sectors
    TestObj.tok("lvchange -r 256 %s/lv3" % vg_name)
    check_lv_expected_value(TestObj, "lv3", vg_name, {"lv_read_ahead": "128.00k"})
    TestObj.tok("lvchange -r none %s/lv3" % vg_name)
    check_lv_expected_value(TestObj, "lv3", vg_name, {"lv_read_ahead": "0 "})
    TestObj.tok("lvchange -r auto %s/lv3" % vg_name)
    check_lv_expected_value(TestObj, "lv3", vg_name, {"lv_read_ahead": "auto"})


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting LV Change Thin Provisioning test")
    print(80 * "#")

    # Create 4 devices
    for dev_num in range(1, 5):
        new_dev = loopdev.create_loopdev(size=128)
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

    if TestObj.trun("lvcreate -V100m -L100m -T %s/pool1 -n lv1" % vg_name) != 0:
        TestObj.tfail("Could not Create pool1")
        return False

    if TestObj.trun("lvcreate -V100m -i2 -L100m -T %s/pool2 -n lv2" % vg_name) != 0:
        TestObj.tfail("Could not Create pool2")
        return False

    _pool_test()
    _lv_test()
    _snapshot_test()

    return True


def _clean_up():
    # TestObj.trun("lvremove -ff %s" % vg_name)
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
