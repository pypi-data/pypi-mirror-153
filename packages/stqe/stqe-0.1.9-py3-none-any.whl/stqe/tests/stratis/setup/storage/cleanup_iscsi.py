#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from time import sleep
from libsan.host.cmdline import run
from libsan.host.linux import hostname
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import clean_var, read_var
from stqe.host.nfs_lock import release_nfs_lock_iscsi


def cleanup_iscsi():
    print("INFO: Cleaning up iSCSI.")
    errors = []

    print("Waiting for data stream to settle before logging out of iscsi.")
    sleep(5)

    disk = read_var("STRATIS_DEVICE")
    if isinstance(disk, list):
        disk = disk[0]
    disk = disk.split("/").pop()
    if "bos" not in hostname():
        atomic_run("Releasing NFS lock on iscsi disk %s." % disk,
                   command=release_nfs_lock_iscsi,
                   disk_name=disk,
                   errors=errors)

    commands = [
        {'message': "Logging out of iSCSI target.", 'cmd': "iscsiadm -m node -u"},
        {'message': "Cleaning targetcli config", 'cmd': "targetcli clearconfig true"},
    ]

    for cmd in commands:
        atomic_run(errors=errors,
                   command=run,
                   **cmd)

    if "brq" not in hostname():
        atomic_run("Removing image file",
                   command=run,
                   cmd="rm -rf /var/tmp/stratis-test.img",
                   errors=errors
                   )

    atomic_run("Cleaning var STRATIS_DEVICE",
               command=clean_var,
               var="STRATIS_DEVICE",
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = cleanup_iscsi()
    exit(parse_ret(errs))
