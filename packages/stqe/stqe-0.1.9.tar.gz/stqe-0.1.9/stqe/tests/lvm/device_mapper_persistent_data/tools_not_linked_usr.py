#!/usr/bin/python

from __future__ import absolute_import, division, print_function, unicode_literals
import stqe.host.tc
from libsan.host.cmdline import run
from libsan.host.linux import install_package
import sys
import re

TC = None


def start_test():
    # Initialize Test Case
    global TC
    TC = stqe.host.tc.TestClass()

    print ("INFO: Making sure tools provided by device_mapper_persistent_data "
           "are not linked to /usr")

    # Paths where we should have no libraries linked from
    lib_paths = ["/usr/"]

    package = "device-mapper-persistent-data"
    install_package(package)
    # Get all tools that we need to check
    ret, output = run("rpm -ql %s | grep \"sbin/\"" % package,
                      return_output=True,
                      verbose=False)
    tools = output.split("\n")

    for tool in tools:
        error = 0
        for lib_path in lib_paths:
            print("INFO: Checking if %s linked to libraries at %s" % (tool, lib_path))
            ret, linked_lib = run("ldd %s" % tool, return_output=True)
            if ret != 0:
                TC.tfail("Could not list dynamically libraries for %s" % (tool))
                error += 1
            else:
                # The command executed sucessfuly
                # check if any library linked is from lib_path
                links = linked_lib.split("\n")
                for link in links:
                    if re.match(".*%s.*" % lib_path, link):
                        TC.tfail("%s is linked to %s" % (tool, link))
                        error += 1

        if error == 0:
            TC.tpass("%s is not linked to /usr/" % tool)

    return True


def main():
    global TC

    start_test()

    if not TC.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: Test pass")
    sys.exit(0)


main()
