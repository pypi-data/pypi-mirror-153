#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import os
from stqe.host.atomic_run import parse_ret, atomic_run
from stqe.host.persistent_vars import read_var, clean_var
from libsan.host.mp import mp_start_service, flush_all, mp_service_name
from libsan.host.linux import is_installed, is_service_running, \
    service_start, service_status, dist_ver


def start_multipath():
    errors = []
    multipath = None
    mp_socket_process = "multipathd.socket"
    if os.path.isfile("/tmp/START_MULTIPATH"):
        multipath = read_var("START_MULTIPATH")

    if not is_installed('device-mapper-multipath'):
        print("WARN: Skipping setup! Package device-mapper-multipath is not installed!")
        return errors

    if multipath is not None and multipath == 1:
        print("WARN: Skipping start of the services because they have not been running!")
        atomic_run("Cleaning var START_MULTIPATH",
                   command=clean_var,
                   var="START_MULTIPATH",
                   errors=errors)
        
        return errors

    if float(dist_ver()) >= 8.0 and not is_service_running(mp_socket_process):
        ret = atomic_run("Starting service %s" % mp_socket_process,
                         service_name=mp_socket_process,
                         command=service_start,
                         errors=errors
                         )
        if ret != 5:
            if not is_service_running(mp_socket_process):
                msg = "FAIL: Service %s is not running" % mp_socket_process
                print(msg)
                errors.append(msg)
                return errors

    atomic_run("Starting service multipathd",
               command=mp_start_service,
               errors=errors
               )

    atomic_run("Flushing all",
               command=flush_all,
               errors=errors
               )

    if not is_service_running(mp_service_name()) and os.path.isfile("/etc/multipath.conf"):
        print("Printing %s status" % mp_service_name())
        service_status(mp_service_name())

        msg = "FAIL: Service %s is not running!" % mp_service_name()
        print(msg)
        errors.append(msg)
        return errors

    return errors


if __name__ == "__main__":
    errs = start_multipath()
    exit(parse_ret(errs))
