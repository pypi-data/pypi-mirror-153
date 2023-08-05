#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.scsi import get_free_disks
from stqe.host.persistent_vars import write_var, read_env
from os import environ
from time import sleep


def get_sync_status(raid_name):
    ret, status = run(return_output=True,
                      cmd="mdadm --detail /dev/md/%s" % raid_name,
                      verbose=False)
    if ret != 0:
        print("WARN: Could not get details on raid %s" % raid_name)
        return None, None
    lines = status.splitlines()
    for line in lines:
        if "State :" in line:
            states = line.split(" : ")[1].split(", ")
            if len(states) == 1 and states[0].strip() == "clean":
                return "clean", True
        elif "Resync Status :" in line or "Rebuild Status :" in line:
            status = line
            return status[0].strip(), False
    print("WARN: It should not get here!")
    return None, None


def wait_for_resync(raid_name, delay=60):
    while 1:
        status, done = get_sync_status(raid_name)
        if done:
            return True
        elif not done and status is not None:
            print("INFO: %s." % status)
        elif done is None and status is None:
            return False
        sleep(delay)


def setup_raid(level, raid_name, wait_resync=False):
    print("INFO: Setting up RAID level %s." % level)
    errors = []

    disks = atomic_run(message="Getting free disks for RAID",
                       command=get_free_disks,
                       errors=errors)
    if disks is None:
        exit(1)
    disks = disks.keys()
    ret, lsblk = atomic_run(message="Listing block devices to check they are really free.",
                            command=run,
                            cmd="lsblk",
                            return_output=True,
                            errors=errors)
    # remove disks that are in use (find only partitioned ones)
    values = [x.strip() for line in lsblk.splitlines() for x in line.split()]
    for disk in [disk for value in values for disk in disks if disk != value and disk in value]:
        disks.remove(disk)

    disk_paths = ["/dev/" + j for j in disks]
    print("Found these free disks: %s" % " ".join(disk_paths))
    for disk in disk_paths:
        atomic_run("Zeroing superblock of disk %s." % disk,
                   command=run,
                   cmd="dd if=/dev/zero of=%s bs=4k count=2" % disk,
                   errors=errors)

    atomic_run("Creating raid %s level %s" % (raid_name, level),
               cmd="mdadm --create %s --level=%s --run --raid-devices=%s %s" %
                   (raid_name, level, len(disk_paths), " ".join(disk_paths)),
               command=run,
               errors=errors)

    run(cmd="mdadm --detail /dev/md/%s" % raid_name,
        verbose=True)

    print(wait_resync)
    if wait_resync:
        # Wait for resync if it is necessary
        atomic_run("Waiting for resync of raid %s" % raid_name,
                   raid_name=raid_name,
                   command=wait_for_resync,
                   errors=errors)

    atomic_run("Writing var VDO_DEVICE",
               command=write_var,
               var={'VDO_DEVICE': "/dev/md/%s" % raid_name},
               errors=errors)

    atomic_run("Writing var RAID_DISKS",
               command=write_var,
               var={'RAID_DISKS': " ".join(disk_paths)},
               errors=errors)

    atomic_run(message="Listing block devices.",
               command=run,
               cmd="lsblk",
               errors=errors)

    # sometimes there is some mess on the dist, clean it up
    atomic_run(message="Cleaning superblock of %s" % raid_name,
               command=run,
               cmd="dd if=/dev/zero of=/dev/md/%s bs=4K count=1" % raid_name,
               errors=errors)

    return errors


if __name__ == "__main__":
    level = 0
    try:
        level = int(environ['fmf_raid_level'])
    except KeyError:
        pass
    except TypeError:
        print("FMF metadata raid_level must be int.")
        exit(1)
    raid_name = "vdo_raid"

    wait_resync = False
    try:
        wait_resync = read_env("fmf_wait_resync")
    except KeyError:
        pass

    errs = setup_raid(level, raid_name, wait_resync=wait_resync)
    exit(parse_ret(errs))
