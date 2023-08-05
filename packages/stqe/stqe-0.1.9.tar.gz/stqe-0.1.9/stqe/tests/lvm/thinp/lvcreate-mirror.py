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


def _mirror():
    global TestObj, vg_name

    #
    # -i|--stripes
    #
    TestObj.tok("lvcreate -L4M --thin %s/pool" % vg_name)
    check_lv_expected_value(TestObj, "[pool_tdata]", vg_name, {"stripes": "1"})

    # --mirror option creates the needed _rimage/data_X LVs
    lvm2_version = linux.package_version("lvm2")
    if not lvm2_version:
        TestObj.tfail("Could not query lvm2 version")
        return

    # Behavior changed on BZ1462712, since then LV must be active to run lvconvert
    # the .el7 should not really matter when comparing versions
    if lvm2_version >= "2.02.171-6.el7":
        TestObj.tok("lvchange -an %s/pool" % vg_name)
        TestObj.tnok("lvconvert --type raid1 --mirrors 3 --yes %s/pool_tdata" % vg_name)
        TestObj.tok("lvchange -ay %s/pool" % vg_name)
    else:
        TestObj.tnok("lvconvert --type raid1 --mirrors 3 --yes %s/pool_tdata" % vg_name)
        TestObj.tok("lvchange -an %s/pool" % vg_name)

    TestObj.tok("lvconvert --type raid1 --mirrors 3 --yes %s/pool_tdata" % vg_name)
    TestObj.tok("lvconvert --type raid1 -m 1 --yes %s/pool_tmeta" % vg_name)
    TestObj.tok("lvchange -ay %s/pool" % vg_name)

    check_lv_expected_value(TestObj, "[pool_tdata_rimage_0]", vg_name, {"stripes": "1"})
    check_lv_expected_value(TestObj, "[pool_tdata_rimage_1]", vg_name, {"stripes": "1"})
    check_lv_expected_value(TestObj, "[pool_tdata_rimage_2]", vg_name, {"stripes": "1"})
    check_lv_expected_value(TestObj, "[pool_tdata_rimage_3]", vg_name, {"stripes": "1"})
    check_lv_expected_value(TestObj, "[pool_tdata_rmeta_0]", vg_name, {"stripes": "1"})
    check_lv_expected_value(TestObj, "[pool_tdata_rmeta_1]", vg_name, {"stripes": "1"})
    check_lv_expected_value(TestObj, "[pool_tdata_rmeta_2]", vg_name, {"stripes": "1"})
    check_lv_expected_value(TestObj, "[pool_tdata_rmeta_3]", vg_name, {"stripes": "1"})

    check_lv_expected_value(TestObj, "[pool_tmeta_rimage_0]", vg_name, {"stripes": "1"})
    check_lv_expected_value(TestObj, "[pool_tmeta_rimage_1]", vg_name, {"stripes": "1"})
    check_lv_expected_value(TestObj, "[pool_tmeta_rmeta_0]", vg_name, {"stripes": "1"})
    check_lv_expected_value(TestObj, "[pool_tmeta_rmeta_1]", vg_name, {"stripes": "1"})

    run("lvs -a %s" % vg_name)
    TestObj.tok("lvremove -ff %s" % vg_name)


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting Thin Provisioning Mirror test")
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

    _mirror()

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
