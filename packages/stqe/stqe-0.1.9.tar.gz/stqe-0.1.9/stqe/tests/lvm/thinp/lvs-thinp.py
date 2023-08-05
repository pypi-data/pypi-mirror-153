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


def _lvs_test():
    TestObj.tok("lvcreate -l1 -T %s/pool1" % vg_name)
    # check_lv_expected_value uses lvs -o help to view the full list of columns available.

    check_lv_expected_value(TestObj, "pool1", vg_name, {"thin_count": "0"})

    # Create a thin LV
    TestObj.tok("lvcreate -V100m -T %s/pool1 -n lv1" % vg_name)
    check_lv_expected_value(TestObj, "pool1", vg_name, {"thin_count": "1"})
    check_lv_expected_value(TestObj, "pool1", vg_name, {"lv_name": "pool1"})
    check_lv_expected_value(TestObj, "pool1", vg_name, {"lv_size": "4.00m"})
    check_lv_expected_value(TestObj, "pool1", vg_name, {"lv_metadata_size": "4.00m"})
    # Since RHEL6.7 lvm2 package, adding 'device (o)pen' bit for lv_attr - 'twi-aotz--', previous is 'twi-a-tz--'.
    # From Zdenek feedback: there is difference we now display 'open' state for thin-pool in use.
    # While in past we have been showing 'open' state for fake thin-pool - now
    # we display 'correct' open stat for read thin-pool device.
    # So once you activate thin volume - thin-pool gets opened.
    # Thus this change should be seen as bugfix, where older versions were
    # basically showing thin pool as unopened device.
    check_lv_expected_value(TestObj, "pool1", vg_name, {"lv_attr": "twi-aotz--"})
    check_lv_expected_value(TestObj, "pool1", vg_name, {"modules": "thin-pool"})
    check_lv_expected_value(TestObj, "pool1", vg_name, {"metadata_lv": "[pool1_tmeta]"})
    check_lv_expected_value(TestObj, "pool1", vg_name, {"data_lv": "[pool1_tdata]"})
    TestObj.tok("lvs %s/pool1 -o+metadata_percent" % vg_name)
    check_lv_expected_value(TestObj, "pool1", vg_name, {"chunksize": "64.00k"})
    check_lv_expected_value(TestObj, "pool1", vg_name, {"transaction_id": "1"})

    check_lv_expected_value(TestObj, "lv1", vg_name, {"pool_lv": "pool1"})
    check_lv_expected_value(TestObj, "lv1", vg_name, {"lv_name": "lv1"})
    check_lv_expected_value(TestObj, "lv1", vg_name, {"lv_size": "100.00m"})
    check_lv_expected_value(TestObj, "lv1", vg_name, {"lv_attr": "Vwi-a-tz--"})
    # Kernel device-mapper modules required for this LV.
    # Since RHEL6.6, the order changed to 'thin,thin-pool', before was 'thin-pool,thin'
    check_lv_expected_value(TestObj, "lv1", vg_name, {"modules": "thin,thin-pool"})

    TestObj.tok("lvs -a %s | egrep '\[pool1_tdata\]\s+%s\s+Twi-ao----'" % (vg_name, vg_name))
    TestObj.tok("lvs -a %s | egrep '\[pool1_tmeta\]\s+%s\s+ewi-ao----'" % (vg_name, vg_name))
    TestObj.tok("lvs -a %s | egrep 'Meta%%'" % vg_name)
    TestObj.tok("lvs -a %s | egrep 'Data%%'" % vg_name)

    # Create another thin LV
    TestObj.tok("lvcreate -V100m -T %s/pool1 -n lv2" % vg_name)
    check_lv_expected_value(TestObj, "pool1", vg_name, {"transaction_id": "2"})
    check_lv_expected_value(TestObj, "pool1", vg_name, {"thin_count": "2"})
    # Since RHEL6.6, the value changed to 'zero', before was '1'
    check_lv_expected_value(TestObj, "pool1", vg_name, {"zero": "zero"})

    # Snapshot
    TestObj.tok("lvcreate -s %s/lv1 -n snap1" % vg_name)
    check_lv_expected_value(TestObj, "pool1", vg_name, {"transaction_id": "3"})
    check_lv_expected_value(TestObj, "pool1", vg_name, {"thin_count": "3"})
    check_lv_expected_value(TestObj, "snap1", vg_name, {"origin": "lv1"})
    check_lv_expected_value(TestObj, "snap1", vg_name, {"lv_name": "snap1"})
    check_lv_expected_value(TestObj, "snap1", vg_name, {"lv_size": "100.00m"})
    check_lv_expected_value(TestObj, "snap1", vg_name, {"lv_attr": "Vwi---tz-k"})
    # Since RHEL6.6, the order changed to 'thin,thin-pool', before was 'thin-pool,thin'
    check_lv_expected_value(TestObj, "snap1", vg_name, {"modules": "thin,thin-pool"})

    # warning messages for thin LV
    # thin pool autoextend
    # Check if warning message is given once the threshold of 80 and 85 are exceeded
    TestObj.tok("grep -E \"^\W+thin_pool_autoextend\" /etc/lvm/lvm.conf")
    TestObj.tok("lvcreate -l25 -V84m -T %s/pool2 -n lv3" % vg_name)
    TestObj.tok("dd if=/dev/zero of=/dev/%s/lv3 bs=1M count=84" % vg_name)
    check_lv_expected_value(TestObj, "lv3", vg_name, {"data_percent": "100.00"})
    check_lv_expected_value(TestObj, "pool2", vg_name, {"data_percent": "84.00"})
    # Wait some time so the message is recorded on system
    linux.sleep(30)
    # on RHEL-6.7 the message is: Thin tsvg-pool-tpool is now 84% full.
    # RHEL-6.8 is: Thin pool tsvg-pool2-tpool data is now 84.00% full.
    TestObj.tok("journalctl -n 100 | grep '%s-pool2-tpool .*is now 84.*%% full'" % vg_name)
    TestObj.tok("lvextend -L88m %s/lv3" % vg_name)
    TestObj.tok("dd if=/dev/zero of=/dev/%s/lv3 bs=1M count=88" % vg_name)
    check_lv_expected_value(TestObj, "lv3", vg_name, {"data_percent": "100.00"})
    check_lv_expected_value(TestObj, "pool2", vg_name, {"data_percent": "88.00"})
    linux.sleep(30)
    TestObj.tok("journalctl -n 100 | grep '%s-pool2-tpool .*is now 88.*%% full'" % vg_name)
    TestObj.tok("lvs %s/pool2 -o+metadata_percent" % vg_name)

    # Check warning level without resizing the LV
    TestObj.tok("lvcreate -L100m -V100m -T %s/pool3 -n lv4" % vg_name)
    thresholds = ["81", "86", "91", "96"]
    for threshold in thresholds:
        TestObj.tok("dd if=/dev/zero of=/dev/%s/lv4 bs=1M count=%s" % (vg_name, threshold))
        check_lv_expected_value(TestObj, "pool3", vg_name, {"data_percent": "%s.00" % threshold})
        linux.sleep(30)
        TestObj.tok("journalctl -n 100 | grep '%s-pool3-tpool .*is now %s.*%% full'" % (vg_name, threshold))

    # test lvs with invalid option
    TestObj.tnok("lvs -o +invalid_option %s/lv1 2>/dev/null" % vg_name)

    TestObj.trun("lvs -a %s" % vg_name)


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting lvs Thin Provisioning test")
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

    _lvs_test()

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
