#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def fs_create_success():
    errors = []

    fs_name = read_var("LSM_FS_NAME")
    fs_size = read_var("LSM_FS_SIZE")
    pool_id = read_var("LSM_POOL_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        ret, data = atomic_run("Creating FS %s with protocol %s." % (fs_name, config['protocol']),
                               command=lsm.fs_create,
                               name=fs_name,
                               size=fs_size,
                               pool=pool_id,
                               return_output=True,
                               errors=errors)
        fs_id = [line.split()[0].strip() for line in data.splitlines() if pool_id in line][0]
        atomic_run("Removing FS %s with protocol %s." % (fs_name, config['protocol']),
                   command=lsm.fs_delete,
                   fs=fs_id,
                   force=True,
                   errors=errors)
    return errors


def fs_create_fail():
    errors = []

    fs_name = read_var("LSM_FS_NAME")
    fs_size = read_var("LSM_FS_SIZE")
    pool_id = read_var("LSM_POOL_ID")
    pool_name = read_var("LSM_POOL_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail creating FS without any paramethers with protocol %s" % config['protocol'],
             'command': lsm.fs_create},
            {'message': "Trying to fail creating FS without name with protocol %s" % config['protocol'],
             'command': lsm.fs_create, 'size': fs_size, 'pool': pool_id},
            {'message': "Trying to fail creating FS without size with protocol %s" % config['protocol'],
             'command': lsm.fs_create, 'name': fs_name, 'pool': pool_id},
            {'message': "Trying to fail creating FS without pool with protocol %s" % config['protocol'],
             'command': lsm.fs_create, 'size': fs_size, 'name': fs_name},
            {'message': "Trying to fail creating FS with wrong size '-1' with protocol %s" % config['protocol'],
             'command': lsm.fs_create, 'size': -1, 'name': fs_name, 'pool': pool_id},
            {'message': "Trying to fail creating FS with wrong size '0' with protocol %s" % config['protocol'],
             'command': lsm.fs_create, 'size': 0, 'name': fs_name, 'pool': pool_id},
            {'message': "Trying to fail creating FS with wrong size 'wrong' with protocol %s" % config['protocol'],
             'command': lsm.fs_create, 'size': "wrong", 'name': fs_name, 'pool': pool_id},
            {'message': "Trying to fail creating FS with pool 'NONEXISTENT' with protocol %s" % config['protocol'],
             'command': lsm.fs_create, 'size': fs_size, 'name': fs_name, 'pool': "NONEXISTENT"},
            {'message': "Trying to fail creating FS with pool name instead of ID with protocol %s" % config['protocol'],
             'command': lsm.fs_create, 'size': fs_size, 'name': fs_name, 'pool': pool_name},
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def fs_create_fail_name_conflict():
    errors = []

    fs_name = read_var("LSM_FS_NAME")
    fs_size = read_var("LSM_FS_SIZE")
    pool_id = read_var("LSM_POOL_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Creating FS %s again to hit NAME CONFLICT with protocol %s." % (fs_name, config['protocol']),
                   command=lsm.fs_create,
                   name=fs_name,
                   size=fs_size,
                   pool=pool_id,
                   expected_ret=4,
                   errors=errors)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = fs_create_success()
    if int(environ['fmf_tier']) == 2:
        errs = fs_create_fail()
        errs += fs_create_fail_name_conflict()
    exit(parse_ret(errs))
