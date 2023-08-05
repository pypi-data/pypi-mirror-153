#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.persistent_vars import write_var
from stqe.host.atomic_run import parse_ret, atomic_run
from libsan.host.mp import mp_stop_service, flush_all, mp_service_name
from libsan.host.linux import is_installed, is_service_running, service_stop


def stop_multipath():
    errors = []
    mp_socket_process = "multipathd.socket"

    if not is_installed('device-mapper-multipath'):
        print("WARN: Skipping setup! Package device-mapper-multipath is not installed!")
        return errors

    if not is_service_running(mp_socket_process) and not is_service_running(mp_service_name()):
        print("WARN: Skipping setup! Services multipathd.service and multipathd.socket are dead!")
        atomic_run("Writing var START_MULTIPATH",
                   command=write_var,
                   var={"START_MULTIPATH": 1},
                   errors=errors)

        return errors

    atomic_run("Stopping service multipathd",
               command=mp_stop_service,
               errors=errors
               )

    atomic_run("Flushing all",
               command=flush_all,
               errors=errors
               )

    if is_service_running(mp_service_name()):
        msg = "FAIL: Service %s is running!" % mp_service_name()
        print(msg)
        errors.append(msg)
        return errors

    if is_service_running(mp_socket_process):
        atomic_run("Stopping service %s" % mp_socket_process,
                   service_name=mp_socket_process,
                   command=service_stop,
                   errors=errors
                   )

        if is_service_running(mp_socket_process):
            msg = "FAIL: Service %s is running!" % mp_socket_process
            print(msg)
            errors.append(msg)
            return errors

    return errors


if __name__ == "__main__":
    errs = stop_multipath()
    exit(parse_ret(errs))
