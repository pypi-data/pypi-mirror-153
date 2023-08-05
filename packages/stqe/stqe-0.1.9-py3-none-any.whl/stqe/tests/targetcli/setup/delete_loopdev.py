#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var
from libsan.host.loopdev import delete_loopdev


def loopdev_delete():
    errors = []

    name = read_var("TARGETCLI_LOOPDEV_NAME")

    atomic_run("Deleting loopdev %s" % name,
               command=delete_loopdev,
               name=name,
               errors=errors
               )

    return errors


if __name__ == "__main__":
    errs = loopdev_delete()
    exit(parse_ret(errs))
