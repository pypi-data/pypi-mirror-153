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
import os
import re
import fileinput
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

lvm_conf_file = "/etc/lvm/lvm.conf"
bk_file = lvm_conf_file + ".copy"


def _get_conf_value(key):
    search_regex = re.compile("\W*%s\s*=\s*(\S+)" % key)
    ret = None
    for line in fileinput.input(lvm_conf_file):
        m = search_regex.match(line)
        if m:
            ret = m.group(1)
    return ret


def _meta_req_sep_pvs():
    lvm.update_config("thin_pool_metadata_require_separate_pvs", "1")
    TestObj.tok("lvcreate -l1 -T %s/pool" % vg_name)
    lv_info = lvm.lv_info("[pool_tdata]", vg_name, "devices")
    if not lv_info:
        TestObj.tfail("Could not device of tdata")
        return
    tdata_dev = lv_info["devices"]
    lv_info = lvm.lv_info("[pool_tmeta]", vg_name, "devices")
    if not lv_info:
        TestObj.tfail("Could not device of tmeta")
        return
    tmeta_dev = lv_info["devices"]
    if tdata_dev == tmeta_dev:
        TestObj.tfail("Expected tmeta an tdata to be in different device")
        run("lvs -a -o+devices")
    else:
        TestObj.tpass("tmeta an tdata are in different devices")
    # Should fail as with 3 stripes there will be no free device for separate metadata
    TestObj.tnok("lvcreate -i3 -l1 -T %s/pool2" % vg_name)

    lvm.update_config("thin_pool_metadata_require_separate_pvs", "0")
    TestObj.tok("lvcreate -l1 -T %s/pool3" % vg_name)
    TestObj.tok("lvcreate -i2 -l1 -T %s/pool4" % vg_name)
    return


def _check_default_values():
    conf = {"thin_pool_autoextend_threshold": "100",
            "thin_pool_autoextend_percent": "20",
            "thin_pool_metadata_require_separate_pvs": "0"}

    for key in conf.keys():
        if _get_conf_value(key) == conf[key]:
            TestObj.tpass("%s == '%s'" % (key, conf[key]))
        else:
            TestObj.tfail(
                "%s == '%s' and not '%s'" % (key, _get_conf_value("thin_pool_autoextend_threshold"), conf[key]))


def start_test():
    global TestObj
    global loop_dev

    print(80 * "#")
    print("INFO: Starting Thin Provisioning lvconf test")
    print(80 * "#")

    # Create 2 devices
    for dev_num in range(1, 3):
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

    _meta_req_sep_pvs()
    _check_default_values()

    return True


def _clean_up():
    global loop_dev, bk_file

    if not lvm.vg_remove(vg_name, force=True):
        TestObj.tfail("Could not delete VG \"%s\"" % vg_name)

    if loop_dev:
        for dev in loop_dev.keys():
            if not lvm.pv_remove(loop_dev[dev]):
                TestObj.tfail("Could not delete PV \"%s\"" % loop_dev[dev])
            linux.sleep(1)
            if not loopdev.delete_loopdev(loop_dev[dev]):
                TestObj.tfail("Could not remove loop device %s" % loop_dev[dev])

    # restore original lvm conf file
    if os.path.isfile(bk_file):
        run("mv -f %s %s" % (bk_file, lvm_conf_file))


def main():
    global TestObj

    TestObj = stqe.host.tc.TestClass()

    linux.install_package("lvm2")

    _clean_up()

    # create backup file
    run("cp -f %s %s" % (lvm_conf_file, bk_file))

    try:
        start_test()
    except Exception as e:
        print(e)
        TestObj.tfail("FAIL: Exception when running test (%s)" % traceback.format_exc())

    _clean_up()

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: test pass")
    sys.exit(0)


main()
