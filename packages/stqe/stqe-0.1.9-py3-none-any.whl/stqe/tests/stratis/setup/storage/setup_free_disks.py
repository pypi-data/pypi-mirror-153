#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.scsi import get_free_disks
from stqe.host.persistent_vars import write_var, read_var, read_env
from libsan.host.linux import is_service_running


def setup_local_disks(number_of_disks):
    msg = "INFO: Getting local disks."
    if number_of_disks:
        msg += " Trying to get %s disks" % number_of_disks
    print(msg)
    errors = []

    disks = atomic_run(message="Getting free disks",
                       command=get_free_disks,
                       errors=errors)
    if disks is None:
        msg = "FAIL: Could not find any free disks."
        print(msg)
        errors.append(msg)
        return errors

    disks = disks.keys()
    disk_paths = ["/dev/" + j for j in disks]
    blockdevs = read_var("STRATIS_DEVICE")

    if blockdevs:
        # backup the previous devices
        atomic_run("Writing var STRATIS_DEVICE_BACKUP",
                   command=write_var,
                   var={'STRATIS_DEVICE_BACKUP': " ".join(blockdevs)},
                   errors=errors)
        if not isinstance(blockdevs, list):
            blockdevs = [blockdevs]
        disk_paths += [x for x in blockdevs if x not in blockdevs]

    if number_of_disks and len(disk_paths) < number_of_disks:
        msg = "WARN: Found only %s disks, need %s disks." % (len(disk_paths), number_of_disks)
        print(msg)
        errors.append(msg)

    print("Using these blockdevs: %s" % " ".join(disk_paths))
    for disk in disk_paths:
        atomic_run("Zeroing superblock of disk %s." % disk,
                   command=run,
                   cmd="dd if=/dev/zero of=%s bs=1M count=10" % disk,
                   errors=errors)
        if is_service_running("multipathd"):
            atomic_run("remove multipath superblock of disk %s." % disk,
                       command=run,
                       cmd="multipath -W %s" % disk,
                       errors=errors)

    atomic_run("Writing var STRATIS_DEVICE",
               command=write_var,
               var={'STRATIS_DEVICE': disk_paths},
               errors=errors)

    atomic_run(message="Listing block devices.",
               command=run,
               cmd="lsblk",
               errors=errors)

    return errors


if __name__ == "__main__":
    try:
        number_of_disks = read_env("fmf_number_of_disks")
    except KeyError:
        number_of_disks = None
    errs = setup_local_disks(number_of_disks)
    exit(parse_ret(errs))
