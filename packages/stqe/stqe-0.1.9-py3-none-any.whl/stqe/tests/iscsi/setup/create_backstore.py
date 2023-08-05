#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, write_var
from libsan.host.lio import TargetCLI
from os import environ


def create_backstore():
    errors = []

    arguments = {
        'name': None,
        'dev': None,
        'file_or_dev': None,
        'size': None,
        'writeback': None,
        'sparse': None,
        'wwn': None,
        'readonly': None,
        'nullio': None,
        'add_mapped_luns': None,
        'lun': None,
        'storage_object': None,
        'ip_address': None,
        'ip_port': None,
        'tag': None,
        'cfgstring': None,
        'hw_max_sectors': None,
        'control': None
    }

    backstore_type = environ["fmf_backstore_type"]

    for arg in arguments.keys():
        try:
            if arg == 'name':
                arguments[arg] = environ['fmf_backstore_name']
                continue
            if arg == "file_or_dev":
                arguments[arg] = "/var/tmp/" + environ["fmf_file_or_dev"]
                continue
            arguments[arg] = environ['fmf_' + arg]
        except KeyError:
            pass

    try:
        loopdev = environ['fmf_loopdev']
    except KeyError:
        loopdev = None
        pass

    if loopdev:
        arguments["dev"] = read_var("TARGETCLI_LOOPDEV_NAME")

    if backstore_type == "user:qcow":
        arguments["cfgstring"] = read_var("IMAGE_PATH") + "/" + read_var("IMAGE_NAME") + ".img"

    target = TargetCLI(path="/backstores/" + backstore_type)

    atomic_run("Creating backstore object with path %s" % target.path,
               command=target.create,
               errors=errors,
               **target.remove_nones(arguments)
               )

    atomic_run("Writing var TARGETCLI_%s_NAME" % backstore_type,
               command=write_var,
               var={backstore_type.upper() + "_NAME": arguments["name"]},
               errors=errors)

    if arguments["file_or_dev"]:
        atomic_run("Writing var FILEIO_FILE",
                   command=write_var,
                   var={"FILEIO_FILE": arguments["file_or_dev"]},
                   errors=errors)

    return errors


if __name__ == "__main__":
    errs = create_backstore()
    exit(parse_ret(errs))
