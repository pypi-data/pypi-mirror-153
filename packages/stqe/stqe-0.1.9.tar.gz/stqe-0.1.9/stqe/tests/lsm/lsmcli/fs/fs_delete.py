#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


# fs_delete_success is part of fs_create_success() in this same directory

def fs_delete_fail():
    errors = []

    fs_name = read_var("LSM_FS_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail deleting FS without name with protocol %s" % config['protocol'],
             'command': lsm.fs_delete},
            {'message': "Trying to fail deleting FS with WRONG name with protocol %s" % config['protocol'],
             'command': lsm.fs_delete, 'fs': "WRONG"},
            {'message': "Trying to fail deleting FS with name instead of ID name with protocol %s" % config['protocol'],
             'command': lsm.fs_delete, 'fs': fs_name},
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 2:
        errs = fs_delete_fail()
    exit(parse_ret(errs))
