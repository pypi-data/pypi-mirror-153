#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lio import TargetCLI
from stqe.host.persistent_vars import read_var
from stqe.host.atomic_run import atomic_run, parse_ret


def delete_iscsi():
    errors = []
    target = TargetCLI(path="/iscsi")
    target_iqn = read_var("TARGET_IQN")

    atomic_run("Deleting iscsi target: %s" % target_iqn,
               wwn=target_iqn,
               command=target.delete,
               errors=errors
               )

    return errors


if __name__ == "__main__":
    errs = delete_iscsi()
    exit(parse_ret(errs))
