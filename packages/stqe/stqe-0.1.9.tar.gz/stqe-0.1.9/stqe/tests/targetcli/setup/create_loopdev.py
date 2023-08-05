#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.persistent_vars import write_var
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.loopdev import create_loopdev
from os import environ


def remove_nones(kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


def loopdev_create():
    errors = []

    args = dict(name=None, size=None)
    for arg in args.keys():
        try:
            args[arg] = environ['fmf_loopdev_%s' % arg]
            if arg == 'size':
                args[arg] = int(args[arg])
        except KeyError:
            pass

    ret = atomic_run("Creating loopdev",
                     command=create_loopdev,
                     errors=errors,
                     **remove_nones(args)
                     )

    atomic_run("Writing var TARGETCLI_LOOPDEV_NAME",
               command=write_var,
               var={"TARGETCLI_LOOPDEV_NAME": ret},
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = loopdev_create()
    exit(parse_ret(errs))
