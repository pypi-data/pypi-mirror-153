#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


# fs_delete_success is part of fs_create_success() in this same directory

def access_group_remove_fail():
    errors = []

    init_id = read_var("LSM_INIT_ID")
    ag_id = read_var("LSM_AG_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail removing initiator from AG without paramethers with protocol %s" % config[
                'protocol'], 'command': lsm.access_group_remove},
            {'message': "Trying to fail removing initiator from AG without ag with protocol %s" % config['protocol'],
             'command': lsm.access_group_remove, 'init': init_id},
            {'message': "Trying to fail removing initiator from AG without init with protocol %s" % config['protocol'],
             'command': lsm.access_group_remove, 'ag': ag_id},
            {'message': "Trying to fail removing initiator from AG with WRONG AG with protocol %s" % config['protocol'],
             'command': lsm.access_group_remove, 'ag': "WRONG", 'init': init_id},
            {'message': "Trying to fail removing initiator from AG with WRONG init with protocol %s" % config[
                'protocol'],
             'command': lsm.access_group_remove, 'ag': ag_id, 'init': "WRONG"}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def access_group_remove_fail_no_state_change():
    errors = []

    init_id_2 = read_var("LSM_INIT_ID_2")
    ag_id = read_var("LSM_AG_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Trying to fail removing wrong initiator from AG to hit NO_STATE_CHANGE "
                   "with protocol %s" % config['protocol'],
                   command=lsm.access_group_remove,
                   ag=ag_id,
                   init=init_id_2,
                   expected_ret=4,
                   errors=errors)
    return errors


def access_group_remove_last_init():
    errors = []

    init_id = read_var("LSM_INIT_ID")
    ag_id = read_var("LSM_AG_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Trying to fail removing last initiator from AG to hit LAST_INIT_IN_ACCESS_GROUP "
                   "with protocol %s" % config['protocol'],
                   command=lsm.access_group_remove,
                   ag=ag_id,
                   init=init_id,
                   expected_ret=4,
                   errors=errors)

    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 2:
        errs = access_group_remove_fail()
        errs += access_group_remove_fail_no_state_change()
        errs += access_group_remove_last_init()
    exit(parse_ret(errs))
