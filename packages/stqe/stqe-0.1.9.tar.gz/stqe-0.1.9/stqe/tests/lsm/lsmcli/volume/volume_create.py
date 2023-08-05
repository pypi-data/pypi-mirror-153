#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def volume_create_success():
    errors = []

    vol_name = read_var("LSM_VOL_NAME")
    vol_size = read_var("LSM_VOL_SIZE")
    pool_id = read_var("LSM_POOL_ID_VOLUME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        for provisioning in [None, "DEFAULT", "THIN", "FULL"]:
            if provisioning is not None:
                provisioning = {'provisioning': provisioning}
            else:
                provisioning = {}
            ret, data = atomic_run("Creating volume %s with protocol %s." % (vol_name, config['protocol']),
                                   command=lsm.volume_create,
                                   name=vol_name,
                                   size=vol_size,
                                   pool=pool_id,
                                   return_output=True,
                                   errors=errors,
                                   **provisioning)
            vol_id = [line.split()[0].strip() for line in data.splitlines() if vol_name in line][0]
            atomic_run("Removing volume %s with protocol %s." % (vol_name, config['protocol']),
                       command=lsm.volume_delete,
                       vol=vol_id,
                       force=True,
                       errors=errors)
    return errors


def volume_create_fail():
    errors = []

    vol_name = read_var("LSM_VOL_NAME")
    vol_size = read_var("LSM_VOL_SIZE")
    pool_id = read_var("LSM_POOL_ID_VOLUME")
    pool_name = read_var("LSM_FS_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail creating volume without any paramethers with protocol %s" % config['protocol'],
             'command': lsm.volume_create},
            {'message': "Trying to fail creating volume without name with protocol %s" % config['protocol'],
             'command': lsm.volume_create, 'size': vol_size, 'pool': pool_id},
            {'message': "Trying to fail creating volume without size with protocol %s" % config['protocol'],
             'command': lsm.volume_create, 'name': vol_name, 'pool': pool_id},
            {'message': "Trying to fail creating volume without pool with protocol %s" % config['protocol'],
             'command': lsm.volume_create, 'size': vol_size, 'name': vol_name},
            {'message': "Trying to fail creating volume with wrong size '-1' with protocol %s" % config['protocol'],
             'command': lsm.volume_create, 'size': -1, 'name': vol_name, 'pool': pool_id},
            {'message': "Trying to fail creating volume with wrong size '0' with protocol %s" % config['protocol'],
             'command': lsm.volume_create, 'size': 0, 'name': vol_name, 'pool': pool_id},
            {'message': "Trying to fail creating volume with wrong size 'wrong' with protocol %s" % config['protocol'],
             'command': lsm.volume_create, 'size': "wrong", 'name': vol_name, 'pool': pool_id},
            {'message': "Trying to fail creating volume with pool 'NONEXISTENT' with protocol %s" % config['protocol'],
             'command': lsm.volume_create, 'size': vol_size, 'name': vol_name, 'pool': "NONEXISTENT"},
            {'message': "Trying to fail creating volume with pool name instead of ID with protocol %s" % config['protocol'],
             'command': lsm.volume_create, 'size': vol_size, 'name': vol_name, 'pool': pool_name},
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def volume_create_fail_name_conflict():
    errors = []

    vol_name = read_var("LSM_VOL_NAME")
    vol_size = read_var("LSM_VOL_SIZE")
    pool_id = read_var("LSM_POOL_ID_VOLUME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Creating volume %s again to hit NAME CONFLICT with protocol %s." % (vol_name, config['protocol']),
                   command=lsm.volume_create,
                   name=vol_name,
                   size=vol_size,
                   pool=pool_id,
                   expected_ret=4,
                   errors=errors)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = volume_create_success()
    if int(environ['fmf_tier']) == 2:
        errs = volume_create_fail()
        errs += volume_create_fail_name_conflict()
    exit(parse_ret(errs))
