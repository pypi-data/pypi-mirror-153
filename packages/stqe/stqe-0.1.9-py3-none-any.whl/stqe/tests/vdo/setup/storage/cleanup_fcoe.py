#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from time import sleep
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import clean_var
from libsan.host.fcoe import unconfigure_soft_fcoe


def cleanup_fcoe():
    print("INFO: Cleaning up soft FCoE.")
    errors = []

    print("Waiting for data stream to settle before cleaning up FCoE.")
    sleep(5)

    atomic_run("Cleaning up FCoE",
               command=unconfigure_soft_fcoe,
               errors=errors)

    atomic_run("Cleaning var VDO_DEVICE",
               command=clean_var,
               var="VDO_DEVICE",
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = cleanup_fcoe()
    exit(parse_ret(errs))
