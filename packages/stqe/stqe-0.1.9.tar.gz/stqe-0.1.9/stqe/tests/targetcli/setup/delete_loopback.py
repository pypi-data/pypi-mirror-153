#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var
from libsan.host.lio import TargetCLI


def loopback_cleanup():
    errors = []
    wwn = read_var("LOOPBACK_WWN")
    lun = "lun" + str(read_var("LOOPBACK_LUN"))
    target = TargetCLI(path="/loopback/%s/luns" % wwn)

    atomic_run("Deleting lun: %s" % lun,
               lun=lun,
               command=target.delete,
               errors=errors
               )

    target.path = "/loopback"

    atomic_run("Deleting loopback: %s" % wwn,
               wwn=wwn,
               command=target.delete,
               errors=errors
               )

    return errors


if __name__ == "__main__":
    errs = loopback_cleanup()
    exit(parse_ret(errs))
