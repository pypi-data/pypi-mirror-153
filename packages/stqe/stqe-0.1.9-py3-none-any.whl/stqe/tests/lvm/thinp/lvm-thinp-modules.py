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
from six.moves import range

TestObj = None

loop_dev = {}

vg_name = "testvg"


def _module_load_unload():
    TestObj.tok("modprobe -r dm_thin_pool")
    print("load & unload dm_thin_pool 100 times")
    TestObj.tok("for i in `seq 100`; do modprobe dm_thin_pool;modprobe -r dm_thin_pool; done")
    # if dm_cache is loaded it also uses dm_persistent_data
    TestObj.tok("modprobe -r dm_cache_cleaner")
    TestObj.tok("modprobe -r dm_cache_smq")
    TestObj.tok("modprobe -r dm_cache")
    TestObj.tok("modprobe -r dm_persistent_data")

    # make sure no thin pool/LV existing and dm-thin-pool & dm-persistent-data are not loaded
    TestObj.tnok("lvs -omodules | grep thin-pool")
    TestObj.tnok("lsmod | egrep -w '^dm_thin_pool'")
    TestObj.tnok("lsmod | egrep -w '^dm_persistent_data'")


def _check_module_value(module, expected_value):
    ret, output = run("lsmod | egrep -w '^%s' | awk '{print $3}'" % module, return_output=True)
    if ret == 0 and output == "%s" % expected_value:
        TestObj.tpass("lsmod | egrep -w '^%s' | awk '{print $3}' == %s" % (module, expected_value))
    else:
        TestObj.tfail("lsmod | egrep -w '^%s' | awk '{print $3}' should return '%s', but returned '%s'" % (
            module, expected_value, output))


def _module_info():
    TestObj.tok("modinfo dm_thin_pool")
    TestObj.tok("modinfo dm_persistent_data")

    TestObj.tok("modinfo -d dm_thin_pool | grep \"^device-mapper thin provisioning target$\"")
    TestObj.tok("modinfo -d dm_persistent_data | grep \"^Immutable metadata library for dm$\"")

    # liner
    TestObj.tok("lvcreate -l1 -T %s/pool1" % vg_name)
    TestObj.tok("lvcreate -V100m -T %s/pool1 -n lv1" % vg_name)
    _check_module_value("dm_persistent_data", "1")
    _check_module_value("dm_thin_pool", "2")

    TestObj.tok("lvcreate -V100m -T %s/pool1 -n lv2" % vg_name)
    _check_module_value("dm_thin_pool", "3")

    # Reduce active pool
    TestObj.tok("lvcreate -l1 -T %s/pool2" % vg_name)
    TestObj.tok("lvcreate -V100m -T %s/pool2 -n lv21" % vg_name)
    _check_module_value("dm_thin_pool", "5")
    TestObj.tok("lvchange -an %s/lv21" % vg_name)
    _check_module_value("dm_thin_pool", "4")
    TestObj.tok("lvchange -an %s/pool2" % vg_name)
    _check_module_value("dm_thin_pool", "3")

    # stripe
    TestObj.tok("lvcreate -i1 -l1 -T %s/pool3" % vg_name)
    TestObj.tok("lvcreate -V100m -T %s/pool3 -n lv31" % vg_name)
    _check_module_value("dm_thin_pool", "5")
    TestObj.tok("lvcreate -V100m -T %s/pool3 -n lv32" % vg_name)
    _check_module_value("dm_thin_pool", "6")

    # reduce pool with stripes
    TestObj.tok("lvcreate -i2 -l1 -T %s/pool4" % vg_name)
    TestObj.tok("lvcreate -V100m -T %s/pool4 -n lv41" % vg_name)
    _check_module_value("dm_thin_pool", "8")
    TestObj.tok("lvchange -an %s/lv41" % vg_name)
    _check_module_value("dm_thin_pool", "7")
    TestObj.tok("lvchange -an %s/pool4" % vg_name)
    _check_module_value("dm_thin_pool", "6")

    TestObj.tok("lsmod | grep -w dm_thin_pool")
    TestObj.tok("lvs -o +modules %s" % vg_name)

    # should NOT be able to unload the module now
    TestObj.tnok("modprobe -r dm_thin_pool")
    TestObj.tok("lsmod | egrep -w '^dm_thin_pool'")
    TestObj.tok("lsmod | egrep -w '^dm_persistent_data'")

    TestObj.tok("lvremove -ff %s" % vg_name)

    # should be able to unload the module now
    TestObj.tok("modprobe -r dm_thin_pool")
    TestObj.tnok("lsmod | egrep -w '^dm_thin_pool'")
    TestObj.tnok("lsmod | egrep -w '^dm_persistent_data'")


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting Thin Provisioning Module test")
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

    _module_load_unload()
    _module_info()

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
        TestObj.tfail("There was some problem while running the test (%s)" % e)
        print(e)

    _clean_up()

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: test pass")
    sys.exit(0)


main()
