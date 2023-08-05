#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import parse_ret
from stqe.host.persistent_vars import read_var, clean_var, write_var


def setup_manual():
    # this just checks if the device is created.
    data = read_var('VDO_DEVICE')

    # remove newline
    if data.endswith('\n'):
        data = data.rstrip('\n')
        clean_var('VDO_DEVICE')
        write_var({'VDO_DEVICE': data})

    print("INFO: Will run tests on device: '%s'" % data)
    return []


if __name__ == "__main__":
    errs = setup_manual()
    exit(parse_ret(errs))
