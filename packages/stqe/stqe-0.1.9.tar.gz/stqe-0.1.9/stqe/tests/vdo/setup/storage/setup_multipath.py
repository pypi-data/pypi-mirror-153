#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, write_var
from libsan.host.mp import get_disks_of_mpath


def setup_multipath():
    disk = read_var("VDO_DEVICE")
    print("INFO: Setting up dm-multipath on device %s." % disk)
    errors = []

    _, mpaths = atomic_run(message="Getting multipaths device",
                             command=run,
                             return_output=True,
                             cmd="multipath -l -v 1",
                             errors=errors)
    mpaths = [mpath.strip() for mpath in mpaths.splitlines()]
    disk = disk.split("/").pop()

    mpath_disk = disk
    for mpath in mpaths:
        possible_disks = get_disks_of_mpath(mpath)
        if disk in possible_disks:
            mpath_disk = "mapper/%s" % mpath

    atomic_run("Writing var VDO_DEVICE",
               command=write_var,
               var={'VDO_DEVICE': "/dev/%s" % mpath_disk},
               errors=errors)

    atomic_run(message="Listing block devices.",
               command=run,
               cmd="lsblk",
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = setup_multipath()
    exit(parse_ret(errs))
