#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, write_var


def setup_crypt():
    disk = read_var("VDO_DEVICE")
    print("INFO: Setting up dm-crypt on device %s." % disk)
    errors = []

    name = "vdo_crypted"

    atomic_run(message="Creating key",
               command=run,
               cmd="echo -e  'y\\n'| ssh-keygen -f key -N redhat",
               errors=errors)

    atomic_run(message="Encrypting disk with dm-crypt/LUKS.",
               command=run,
               cmd="cryptsetup luksFormat %s key --batch-mode" % disk,
               errors=errors)

    atomic_run(message="Opening encrypted disk.",
               command=run,
               cmd="cryptsetup luksOpen %s %s -d key" % (disk, name),
               errors=errors)

    atomic_run("Writing var VDO_DEVICE",
               command=write_var,
               var={'VDO_DEVICE': "/dev/mapper/%s" % name},
               errors=errors)

    atomic_run("Writing var CRYPTED_DISK",
               command=write_var,
               var={'CRYPTED_DISK': "%s" % disk},
               errors=errors)

    atomic_run(message="Listing block devices.",
               command=run,
               cmd="lsblk",
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = setup_crypt()
    exit(parse_ret(errs))
