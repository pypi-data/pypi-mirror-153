#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.loopdev import create_loopdev, get_loopdev
from stqe.host.persistent_vars import write_var, read_var, read_env


def setup_loop_devs(number_of_loopdevs):
    errors = []

    if not number_of_loopdevs:
        number_of_loopdevs = 2

    for i in range(number_of_loopdevs):
        atomic_run("Creating loop device number %s" % i,
                   command=create_loopdev,
                   errors=errors
                   )

    loopdevs = atomic_run(message="Gettting loop devices",
                          command=get_loopdev,
                          errors=errors)

    blockdevs = read_var("STRATIS_DEVICE")

    if blockdevs:
        # backup the previous devices
        atomic_run("Writing var STRATIS_DEVICE_BACKUP",
                   command=write_var,
                   var={'STRATIS_DEVICE_BACKUP': " ".join(blockdevs)},
                   errors=errors)
        if not isinstance(blockdevs, list):
            blockdevs = [blockdevs]
        loopdevs += [x for x in blockdevs if x not in blockdevs]

    if number_of_loopdevs and len(loopdevs) < number_of_loopdevs:
        msg = "WARN: Found only %s disks, need %s disks." % (len(loopdevs), number_of_loopdevs)
        print(msg)
        errors.append(msg)

    print("Using these blockdevs: %s" % " ".join(loopdevs))
    for disk in loopdevs:
        atomic_run("Zeroing superblock of disk %s." % disk,
                   command=run,
                   cmd="dd if=/dev/zero of=%s bs=1M count=10" % disk,
                   errors=errors)
        atomic_run("remove multipath superblock of disk %s." % disk,
                   command=run,
                   cmd="multipath -W %s" % disk,
                   errors=errors)

    atomic_run("Writing var STRATIS_DEVICE",
               command=write_var,
               var={'STRATIS_DEVICE': loopdevs},
               errors=errors)

    atomic_run(message="Listing block devices.",
               command=run,
               cmd="lsblk",
               errors=errors)

    return errors


if __name__ == "__main__":
    try:
        number_of_loopdevs = read_env("fmf_number_of_disks")
    except KeyError:
        number_of_loopdevs = None
    errs = setup_loop_devs(number_of_loopdevs)
    exit(parse_ret(errs))
