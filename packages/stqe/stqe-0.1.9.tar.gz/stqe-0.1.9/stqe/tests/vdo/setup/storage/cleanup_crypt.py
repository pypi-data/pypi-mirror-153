#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import clean_var, read_var, write_var


def cleanup_crypt():
    disk = read_var("CRYPTED_DISK")
    print("INFO: Cleaning up dm-crypt from device %s." % disk)
    errors = []

    crypted_device = read_var("VDO_DEVICE")

    atomic_run(message="Closing LUKS device %s." % crypted_device,
               command=run,
               cmd="cryptsetup luksClose %s" % crypted_device,
               errors=errors)

    atomic_run(message="Removing LUKS signature from disk %s." % disk,
               command=run,
               cmd="wipefs --all %s" % disk,
               errors=errors)

    atomic_run("Cleaning var CRYPTED_DISK",
               command=clean_var,
               var="CRYPTED_DISK",
               errors=errors)

    atomic_run("Writing var VDO_DEVICE",
               command=write_var,
               var={'VDO_DEVICE': "%s" % disk},
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = cleanup_crypt()
    exit(parse_ret(errs))
