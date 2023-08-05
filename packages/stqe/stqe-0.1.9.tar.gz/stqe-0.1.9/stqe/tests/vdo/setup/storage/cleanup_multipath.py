#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from libsan.host.linux import wait_udev
from stqe.host.atomic_run import atomic_run, parse_ret


def cleanup_multipath():
    print("INFO: Removing multipath.")
    errors = []

    ret, multipath = atomic_run(message="Getting mpath device",
                                command=run,
                                return_output=True,
                                cmd="multipath -l -v 1",
                                errors=errors)

    cmd = "-F"
    if multipath is not None:
        cmd = "-f %s" % multipath
    for mpath in cmd.splitlines():
        if '-' not in mpath:
            mpath = '-f ' + mpath
        atomic_run(message="Removing mpath device %s" % multipath,
                   command=run,
                   cmd="multipath %s" % mpath,
                   errors=errors)

    # wait for udevadm to settle
    wait_udev()

    return errors


if __name__ == "__main__":
    errs = cleanup_multipath()
    exit(parse_ret(errs))
