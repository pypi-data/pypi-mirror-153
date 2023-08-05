#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def access_group_create_success():
    errors = []

    ag_name = read_var("LSM_AG_NAME")
    sys_id = read_var("LSM_SYS_ID")
    init_id = read_var("LSM_INIT_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        ret, data = atomic_run("Creating AG %s with protocol %s." % (ag_name, config['protocol']),
                               command=lsm.access_group_create,
                               name=ag_name,
                               init=init_id,
                               sys=sys_id,
                               return_output=True,
                               errors=errors)
        ag_id = [line.split()[0].strip() for line in data.splitlines() if ag_name in line][0]
        atomic_run("Deleting AG %s with protocol %s." % (ag_name, config['protocol']),
                   command=lsm.access_group_delete,
                   ag=ag_id,
                   force=True,
                   errors=errors)
    return errors


def access_group_create_fail():
    errors = []

    ag_name = read_var("LSM_AG_NAME")
    sys_id = read_var("LSM_SYS_ID")
    init_id = read_var("LSM_INIT_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail creating AG without any paramethers with protocol %s" % config['protocol'],
             'command': lsm.access_group_create},
            {'message': "Trying to fail creating AG without name with protocol %s" % config['protocol'],
             'command': lsm.access_group_create, 'sys': sys_id, 'init': init_id},
            {'message': "Trying to fail creating AG without init with protocol %s" % config['protocol'],
             'command': lsm.access_group_create, 'sys': sys_id, 'name': ag_name},
            {'message': "Trying to fail creating AG without sys with protocol %s" % config['protocol'],
             'command': lsm.access_group_create, 'init': init_id, 'name': ag_name},
            {'message': "Trying to fail creating AG with wrong init '-1' with protocol %s" % config['protocol'],
             'command': lsm.access_group_create, 'init': -1, 'name': ag_name, 'sys': sys_id},
            {'message': "Trying to fail creating AG with NONEXISTENT sys with protocol %s" % config['protocol'],
             'command': lsm.access_group_create, 'init': init_id, 'name': ag_name, 'sys': "NONEXISTENT"},
            {'message': "Trying to fail creating AG with NONEXISTENT init with protocol %s" % config['protocol'],
             'command': lsm.access_group_create, 'init': "NONEXISTENT", 'name': ag_name, 'sys': sys_id}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def access_group_create_fail_name_conflict():
    errors = []

    ag_name = read_var("LSM_AG_NAME")
    sys_id = read_var("LSM_SYS_ID")
    init_id = read_var("LSM_INIT_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Creating AG %s to hit NAME CONFLICT with protocol %s." % (ag_name, config['protocol']),
                   command=lsm.access_group_create,
                   name=ag_name,
                   init=init_id,
                   sys=sys_id,
                   expected_ret=4,
                   errors=errors)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = access_group_create_success()
    if int(environ['fmf_tier']) == 2:
        errs = access_group_create_fail()
        errs += access_group_create_fail_name_conflict()
    exit(parse_ret(errs))
