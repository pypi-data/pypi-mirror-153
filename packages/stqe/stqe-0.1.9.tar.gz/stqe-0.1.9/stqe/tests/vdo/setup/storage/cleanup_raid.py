#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, clean_var


def cleanup_raid():
    raid = read_var('VDO_DEVICE')
    print("INFO: Cleaning up raid %s" % raid)
    errors = []

    atomic_run("Stopping raid %s" % raid,
               cmd="mdadm --stop %s" % raid,
               command=run,
               errors=errors)

    disks = read_var('RAID_DISKS')
    atomic_run("Zeroing superblock on disks: %s" % disks,
               cmd="mdadm --zero-superblock %s" % disks,
               command=run,
               errors=errors)

    atomic_run("Cleaning var VDO_DEVICE",
               command=clean_var,
               var="VDO_DEVICE",
               errors=errors)

    atomic_run("Cleaning var RAID_DISKS",
               command=clean_var,
               var="RAID_DISKS",
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = cleanup_raid()
    exit(parse_ret(errs))
