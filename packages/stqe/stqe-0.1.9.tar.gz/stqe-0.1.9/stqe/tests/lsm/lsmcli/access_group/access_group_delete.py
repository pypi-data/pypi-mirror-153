#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


# fs_delete_success is part of fs_create_success() in this same directory

def access_group_delete_fail():
    errors = []

    init_id = read_var("LSM_INIT_ID")
    sys_id = read_var("LSM_SYS_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail deleting AG without paramethers with protocol %s" % config['protocol'],
             'command': lsm.access_group_delete},
            {'message': "Trying to fail deleting AG with WRONG AG with protocol %s" % config['protocol'],
             'command': lsm.access_group_delete, 'ag': "WRONG"},
            {'message': "Trying to fail deleting AG with init ID instead of AG ID name with protocol %s" % config['protocol'],
             'command': lsm.access_group_delete, 'ag': init_id},
            {'message': "Trying to fail deleting AG with sys ID instead of AG ID name with protocol %s" % config['protocol'],
             'command': lsm.access_group_delete, 'ag': sys_id},
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 2:
        errs = access_group_delete_fail()
    exit(parse_ret(errs))
