#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import clean_var


def cleanup_configure():
    print("INFO: Cleaning up libstoragemgmt configurations.")
    errors = []

    ret, variables = atomic_run("Getting variables to clean.",
                                command=run,
                                cmd="ls -la /tmp",
                                return_output=True,
                                errors=errors)

    variables = [value for line in variables.splitlines() for value in line.split() if value.startswith("LSM_")]
    print("Will clean these variables: %s" % " ".join(variables))

    for var in variables:
        atomic_run("Cleaning var %s" % var,
                   command=clean_var,
                   var=var,
                   errors=errors)

    return errors


if __name__ == "__main__":
    errs = cleanup_configure()
    exit(parse_ret(errs))
