#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.lio import TargetCLI
from os import environ


def saveconfig_create():
    errors = []
    target = TargetCLI(path="")

    args = dict(savefile=None)
    try:
        args["savefile"] = environ['fmf_savefile_name']
    except KeyError:
        pass

    atomic_run("Creating saveconfig",
               command=target.saveconfig,
               errors=errors,
               **target.remove_nones(args)
               )

    return errors


if __name__ == "__main__":
    errs = saveconfig_create()
    exit(parse_ret(errs))
