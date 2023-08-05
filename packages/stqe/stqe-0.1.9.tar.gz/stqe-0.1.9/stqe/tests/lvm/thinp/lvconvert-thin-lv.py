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
import libsan.host.linux as linux
import libsan.host.loopdev as loopdev
from stqe.host.lvm import check_lv_expected_value
from six.moves import range

TestObj = None

loop_dev = {}

vg_name = "testvg"
mount_point = "/mnt/thin"


def _convert():
    global TestObj, vg_name, mount_point

    thin_device = "/dev/mapper/%s-thin" % vg_name
    thin_origin_device = "/dev/mapper/%s-thin_origin" % vg_name

    # Convert an LV to be used as thin LV
    TestObj.tok("lvcreate -l25 -n %s/thin" % vg_name)
    linux.mkdir(mount_point)
    fs = linux.get_default_fs()
    if not linux.mkfs(thin_device, fs, force=True):
        TestObj.tfail("Could not create file system (%s)" % fs)
        return False

    if not linux.mount(thin_device, mount_point):
        TestObj.tfail("Could not mount device")
        return False
    TestObj.tok("dd if=/dev/urandom of=%s/5m bs=1M count=5;sync" % mount_point)
    TestObj.tok("md5sum %s/5m > pre_md5" % mount_point)

    TestObj.tok("lvcreate -l50 -T -n %s/pool" % vg_name)
    TestObj.tlog("test case:1")
    # https://bugzilla.redhat.com/show_bug.cgi?id=997704#c5
    TestObj.tok("lvconvert --thinpool %s/pool --thin %s/thin --originname thin_origin -y" % (vg_name, vg_name))
    linux.sync()
    # Make sure there was no data corruption
    TestObj.tlog("1.1 checking if the md5 checksum is not changed")
    TestObj.tok("md5sum %s/5m > post_md5" % mount_point)
    TestObj.tok("diff pre_md5 post_md5")

    TestObj.tlog("1.2 checking if the thin LV is converted")
    check_lv_expected_value(TestObj, "thin", vg_name,
                            {"lv_size": "100.00m", "pool_lv": "pool",
                             "lv_attr": "Vwi-aotz--", "origin": "thin_origin"})

    TestObj.tlog("1.3 checking if a readonly lv is created for the pre-data")
    check_lv_expected_value(TestObj, "thin_origin", vg_name, {"lv_attr": "ori-------"})

    TestObj.tlog("1.4 checking if the new data will be stored in the pool")
    lv_info = lvm.lv_info("thin", vg_name, "data_percent")
    if not lv_info:
        TestObj.tfail("Could not query data_percent from thin LV")
        return False
    pre_thin_dp = float(lv_info["data_percent"])
    lv_info = lvm.lv_info("pool", vg_name, "data_percent")
    if not lv_info:
        TestObj.tfail("Could not query data_percent from thin LV")
        return False
    pre_pool_dp = float(lv_info["data_percent"])

    TestObj.tok("dd if=/dev/urandom of=%s/10m bs=1M count=10;sync" % mount_point)
    lv_info = lvm.lv_info("thin", vg_name, "data_percent")
    if not lv_info:
        TestObj.tfail("Could not query data_percent from thin LV")
        return False
    post_thin_dp = float(lv_info["data_percent"])
    lv_info = lvm.lv_info("pool", vg_name, "data_percent")
    if not lv_info:
        TestObj.tfail("Could not query data_percent from thin LV")
        return False
    post_pool_dp = float(lv_info["data_percent"])
    if post_thin_dp > pre_thin_dp and post_pool_dp > pre_pool_dp:
        TestObj.tpass("Data percentage increased correctly")
    else:
        TestObj.tfail("Data percentage did not increase")

    TestObj.tlog("1.5 checking deleting the pre-data, the origin will not impact")
    TestObj.tok("rm -rf %s/5m" % mount_point)
    if not linux.umount(mount_point):
        TestObj.tfail("Could not umount device")
        return False

    TestObj.tok("lvremove -ff %s/thin" % vg_name)
    TestObj.tok("lvchange -ay %s/thin_origin" % vg_name)

    if fs == "xfs":
        # XFS needs  'writable' device to  be able to work with journal
        TestObj.tok("lvchange -prw %s/thin_origin" % vg_name)

    if not linux.mount(thin_origin_device, mount_point):
        TestObj.tfail("Could not mount thin origin device")
        return False
    TestObj.tok("md5sum %s/5m > origin_md5" % mount_point)
    TestObj.tok("diff pre_md5 origin_md5")


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting Thin Pool Convert test")
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

    _convert()

    return True


def _clean_up():
    linux.umount(mount_point)

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
        print(e)
        traceback.print_exc()
        TestObj.tfail("There was some problem while running the test (%s)" % e)

    _clean_up()

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: test pass")
    sys.exit(0)


main()
