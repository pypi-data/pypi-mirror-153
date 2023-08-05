#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def access_group_add_success():
    errors = []

    ag_id = read_var("LSM_AG_ID")
    init_id = read_var("LSM_INIT_ID_2")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Adding initiator %s to AG %s with protocol %s." % (init_id, ag_id, config['protocol']),
                   command=lsm.access_group_add,
                   ag=ag_id,
                   init=init_id,
                   errors=errors)

        atomic_run("Removing initiator %s from AG %s with protocol %s." % (init_id, ag_id, config['protocol']),
                   command=lsm.access_group_remove,
                   ag=ag_id,
                   init=init_id,
                   force=True,
                   errors=errors)
    return errors


def access_group_add_fail():
    errors = []

    ag_name = read_var("LSM_AG_NAME")
    ag_id = read_var("LSM_AG_ID")
    init_id = read_var("LSM_INIT_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail adding initiator to AG without any paramethers with protocol %s" % config[
                'protocol'],
             'command': lsm.access_group_add},
            {'message': "Trying to fail adding initiator to AG without AG with protocol %s" % config['protocol'],
             'command': lsm.access_group_add, 'init': init_id},
            {'message': "Trying to fail adding initiator to AG without init with protocol %s" % config['protocol'],
             'command': lsm.access_group_add, 'ag': ag_id},
            {'message': "Trying to fail adding initiator to AG with wrong init '-1' with protocol %s" % config[
                'protocol'], 'command': lsm.access_group_add, 'init': -1, 'ag': ag_id},
            {'message': "Trying to fail adding initiator to AG with NONEXISTENT AG with protocol %s" % config[
                'protocol'], 'command': lsm.access_group_add, 'init': init_id, 'ag': "NONEXISTENT"},
            {'message': "Trying to fail adding initiator to AG with NONEXISTENT init with protocol %s" % config[
                'protocol'], 'command': lsm.access_group_add, 'init': "NONEXISTENT", 'ag': ag_id},
            {'message': "Trying to fail adding initiator to AG with AG name instead of AG ID with protocol %s" % config[
                'protocol'], 'command': lsm.access_group_add, 'init': init_id, 'ag': ag_name}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def access_group_add_fail_no_state_change():
    errors = []

    ag_id = read_var("LSM_AG_ID")
    init_id = read_var("LSM_INIT_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Adding initiator %s to AG %s to hit NO STATE CHANGE "
                   "with protocol %s." % (init_id, ag_id, config['protocol']),
                   command=lsm.access_group_add,
                   ag=ag_id,
                   init=init_id,
                   expected_ret=4,
                   errors=errors)
    return errors


def access_group_add_fail_exists_initiator():
    errors = []

    ag_name_2 = read_var("LSM_AG_NAME_2")
    sys_id = read_var("LSM_SYS_ID")
    init_id_2 = read_var("LSM_INIT_ID_2")
    ag_id = read_var("LSM_AG_ID")
    init_id = read_var("LSM_INIT_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        ret, data = atomic_run("Creating AG_2 %s with protocol %s." % (ag_name_2, config['protocol']),
                               command=lsm.access_group_create,
                               name=ag_name_2,
                               init=init_id_2,
                               sys=sys_id,
                               return_output=True,
                               errors=errors)
        ag_id_2 = [line.split()[0].strip() for line in data.splitlines() if ag_name_2 in line][0]

        atomic_run("Adding initiator %s to AG %s to hit EXISTS_INITIATOR "
                   "with protocol %s." % (init_id, ag_id, config['protocol']),
                   command=lsm.access_group_add,
                   ag=ag_id,
                   init=init_id_2,
                   expected_ret=4,
                   errors=errors)

        atomic_run("Deleting AG_2 %s with protocol %s." % (ag_name_2, config['protocol']),
                   command=lsm.access_group_delete,
                   ag=ag_id_2,
                   force=True,
                   errors=errors)

    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = access_group_add_success()
    if int(environ['fmf_tier']) == 2:
        errs = access_group_add_fail()
        errs += access_group_add_fail_no_state_change()
        errs += access_group_add_fail_exists_initiator()
    exit(parse_ret(errs))
