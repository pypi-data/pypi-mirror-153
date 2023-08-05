#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from time import sleep
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import clean_var, read_var, write_var


def cleanup_free_disks():
    print("INFO: Cleaning up free disks to previous state.")
    errors = []

    print("Waiting for data stream to settle before logging out of iscsi.")
    sleep(5)

    atomic_run("Cleaning var STRATIS_DEVICE",
               command=clean_var,
               var="STRATIS_DEVICE",
               errors=errors)

    backup = read_var("STRATIS_DEVICE_BACKUP")
    if backup:
        atomic_run("Cleaning var STRATIS_DEVICE_BACKUP",
                   command=clean_var,
                   var="STRATIS_DEVICE_BACKUP",
                   errors=errors)

        atomic_run("Writing var STRATIS_DEVICE",
                   command=write_var,
                   var={'STRATIS_DEVICE': backup},
                   errors=errors)

    return errors


if __name__ == "__main__":
    errs = cleanup_free_disks()
    exit(parse_ret(errs))
