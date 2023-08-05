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

# Regression test for:
# BZ1311818 - software iSCSI: Data corruption occured with 4K I/O is sent repeatedly during ethernet port failure tests

from __future__ import absolute_import, division, print_function, unicode_literals
import libsan.host.dt as dt
import libsan.host.linux as linux
import libsan.host.mp as mp
import libsan.host.fcoe as fcoe
import libsan.sanmgmt as sanmgmt
import stqe.host.tc
import sys
import os
import traceback
import argparse

TestObj = None

runtime = "1h"

test_ifaces = []
obj_sanmgmt = None


def start_test():
    global TestObj, obj_sanmgmt, test_ifaces, runtime

    print(80 * "#")
    print("INFO: Starting alternate interface failover test")
    print(80 * "#")

    _clean_up()

    choosen_devs = sanmgmt.choose_mpaths()
    if not choosen_devs:
        TestObj.tfail("Could not find any device to perform IO")
        return False

    for dev_name in choosen_devs.keys():
        test_device = "/dev/mapper/%s" % dev_name
        print("INFO: Starting IO test on %s" % test_device)
        mp_info = mp.multipath_query_all(dev_name)
        if not mp_info:
            TestObj.tfail("Could not query info for %s" % dev_name)
            return False

        obj_sanmgmt = sanmgmt.create_sanmgmt_for_mpath(dev_name)
        if not obj_sanmgmt:
            TestObj.tfail("Could not create SanMgmt obj")
            return False

        test_ifaces = []
        # If it list is empty nothing will be added
        test_ifaces.extend(mp_info["h_wwpns"])
        # We use MAC interface for iSCSI devices
        test_ifaces.extend(mp_info["iface_macs"])

        if len(test_ifaces) < 2:
            TestObj.tfail("Mpath device %s has less than 2 host interfaces" % dev_name)
            print(test_ifaces)
            return False

        flag_dt_done = 0
        exit_status = 1
        dt_pid = dt.dt_stress_background(of="/dev/mapper/%s" % dev_name, time=runtime)
        while flag_dt_done == 0:
            for iface in test_ifaces:
                mp.multipath_show()
                if not obj_sanmgmt.link_down(iface):
                    TestObj.tfail("Could not bring %s down" % iface)
                    return False
                print("INFO: Waiting 40s with %s DOWN" % iface)
                linux.sleep(40)
                if not obj_sanmgmt.link_up(iface):
                    TestObj.tfail("Could not bring %s up" % iface)
                    return False
                print("INFO: Waiting 600s with all ifaces UP")
                # wait a bit to allow multipath detect the path is restored
                linux.sleep(600)

                flag_dt_done, exit_status = os.waitpid(dt_pid, os.WNOHANG)
                if flag_dt_done:
                    break

        if exit_status == 0:
            return True

    return False


def _clean_up():
    global obj_sanmgmt, test_ifaces

    if not obj_sanmgmt:
        return True

    # make sure the interfaces will be up when test finishes
    for iface in test_ifaces:
        obj_sanmgmt.link_up(iface)


def main():
    global TestObj, runtime

    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", "-t", required=False, dest="runtime",
                        help="runtime", metavar="time")

    args = parser.parse_args()
    if args.runtime:
        runtime = args.runtime

    # Environment variable will have preference over parameter value
    if "RUNTIME" in list(os.environ.keys()):
        runtime = os.environ['RUNTIME']

    # Try to enable SW FCoE and iSCSI
    fcoe.setup_soft_fcoe()
    sanmgmt.setup_iscsi()

    TestObj = stqe.host.tc.TestClass()

    try:
        start_test()
    except Exception as e:
        print(e)
        # traceback.print_exc()
        # e = sys.exc_info()[0]
        TestObj.tfail("FAIL: Exception when running test (%s)" % traceback.format_exc())

    _clean_up()

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: Test pass")
    sys.exit(0)


main()
