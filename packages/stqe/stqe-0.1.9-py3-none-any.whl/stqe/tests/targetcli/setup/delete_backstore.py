#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var
from libsan.host.lio import TargetCLI
from libsan.host.cmdline import run
import os


def delete_backstore():
    errors = []

    arguments = {
        "wwn": None,
        "lun": None,
        "ip_address": None,
        "ip_port": None,
        "tag": None
    }

    fileio_file = None
    path = os.environ["fmf_backstore"]
    if path == "fileio":
        fileio_file = read_var("FILEIO_FILE")

    for arg in arguments.keys():
        try:
            arguments[arg] = os.environ['fmf_' + arg]
        except KeyError:
            pass

    arguments["name"] = read_var(path.upper() + "_NAME")

    target = TargetCLI(path="/backstores/%s" % path)

    atomic_run("Deleting bacstore %s" % arguments["name"],
               command=target.delete,
               errors=errors,
               **target.remove_nones(arguments)
               )

    if fileio_file and os.path.isfile(fileio_file):
        atomic_run("Removing file ",
                   cmd="rm -f %s" % fileio_file,
                   command=run,
                   errors=errors
                   )

    return errors


if __name__ == "__main__":
    errs = delete_backstore()
    exit(parse_ret(errs))
