#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


# volume_delete_success is part of volume_create_success() in this same directory

def volume_delete_fail():
    errors = []

    vol_name = read_var("LSM_VOL_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail deleting volume without paramethers with protocol %s" % config['protocol'],
             'command': lsm.volume_delete},
            {'message': "Trying to fail deleting volume with WRONG name with protocol %s" % config['protocol'],
             'command': lsm.volume_delete, 'vol': "WRONG"},
            {'message': "Trying to fail deleting volume with name instead of ID with protocol %s" % config['protocol'],
             'command': lsm.volume_delete, 'vol': vol_name},
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def volume_delete_child_dependency():
    errors = []
    # TODO: test HAS_CHILD_DEPENDENCY(161): Requested volume has child dependency
    return errors

if __name__ == "__main__":
    if int(environ['fmf_tier']) == 2:
        errs = volume_delete_fail()
    exit(parse_ret(errs))
