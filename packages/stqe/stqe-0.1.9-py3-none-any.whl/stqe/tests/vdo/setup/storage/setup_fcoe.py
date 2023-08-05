#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.fcoe import setup_soft_fcoe
from libsan.sanmgmt import choose_mpaths
from stqe.host.persistent_vars import write_var


def setup_fcoe():
    print("INFO: Setting up FCoE.")
    errors = []

    atomic_run("Setting up soft FCoE",
               command=setup_soft_fcoe,
               errors=errors)

    mpaths = atomic_run(message="Getting multipath information",
                        command=choose_mpaths,
                        errors=errors)

    disk = None
    for mpath in mpaths:
        if 'FCoE' in mpaths[mpath]['transport_types']:
            disk = mpaths[mpath]['disk'].keys().pop()

    if not disk:
        msg = "FAIL: Could not find FCoE disk."
        print(msg)
        errors += msg
        return errors

    atomic_run("Cleaning superblock of device /dev/%s" % disk,
               command=run,
               cmd="dd if=/dev/zero of=/dev/%s bs=4k count=2" % disk,
               errors=errors)

    atomic_run("Writing var VDO_DEVICE",
               command=write_var,
               var={'VDO_DEVICE': "/dev/%s" % disk},
               errors=errors)

    atomic_run("Listing block devices.",
               command=run,
               cmd="lsblk",
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = setup_fcoe()
    exit(parse_ret(errs))
