#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def fs_snap_create_success():
    errors = []

    snap_name = read_var("LSM_FS_SNAP_NAME")
    fs_id = read_var("LSM_FS_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        ret, data = atomic_run("Creating snapshot %s on FS %s with protocol %s." %
                               (snap_name, fs_id, config['protocol']),
                               command=lsm.fs_snap_create,
                               name=snap_name,
                               fs=fs_id,
                               return_output=True,
                               errors=errors)
        snap_id = [line.split()[0].strip() for line in data.splitlines() if snap_name in line][0]
        atomic_run("Removing snapshot %s from FS %s with protocol %s." % (snap_id, fs_id, config['protocol']),
                   command=lsm.fs_snap_delete,
                   snap=snap_id,
                   fs=fs_id,
                   force=True,
                   errors=errors)
    return errors


def fs_snap_create_fail():
    errors = []

    snap_name = read_var("LSM_FS_SNAP_NAME")
    fs_id = read_var("LSM_FS_ID")
    fs_name = read_var("LSM_FS_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail creating snapshot on FS without any paramethers with protocol %s"
                        % config['protocol'], 'command': lsm.fs_snap_create},
            {'message': "Trying to fail creating snapshot on FS without 'fs' with protocol %s" % config['protocol'],
             'command': lsm.fs_snap_create, 'name': snap_name},
            {'message': "Trying to fail creating snapshot on FS without 'name' with protocol %s" % config['protocol'],
             'command': lsm.fs_snap_create, 'fs': fs_id},
            {'message': "Trying to fail creating snapshot on FS by using fs-name instead of fs-ID with protocol %s"
                        % config['protocol'], 'command': lsm.fs_snap_create, 'fs': fs_name, 'name': snap_name},
            {'message': "Trying to fail creating snapshot on NONEXISTENT FS with protocol %s" % config['protocol'],
             'command': lsm.fs_snap_create, 'fs': "NONEXISTENT", 'name': snap_name},
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def fs_snap_create_fail_name_conflict():
    errors = []

    snap_name = read_var("LSM_FS_SNAP_NAME")
    fs_id = read_var("LSM_FS_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        ret, data = atomic_run("Creating snapshot %s on FS %s with protocol %s." %
                               (snap_name, fs_id, config['protocol']),
                               command=lsm.fs_snap_create,
                               name=snap_name,
                               fs=fs_id,
                               return_output=True,
                               errors=errors)
        snap_id = [line.split()[0].strip() for line in data.splitlines() if snap_name in line][0]

        atomic_run("Creating snapshot %s on FS %s again to hit name conflict with protocol %s." %
                   (snap_name, fs_id, config['protocol']),
                   command=lsm.fs_snap_create,
                   name=snap_name,
                   fs=fs_id,
                   expected_ret=4,
                   errors=errors)

        atomic_run("Removing snapshot %s from FS %s with protocol %s." % (snap_id, fs_id, config['protocol']),
                   command=lsm.fs_snap_delete,
                   snap=snap_id,
                   fs=fs_id,
                   force=True,
                   errors=errors)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = fs_snap_create_success()
    if int(environ['fmf_tier']) == 2:
        errs = fs_snap_create_fail()
        errs += fs_snap_create_fail_name_conflict()
    exit(parse_ret(errs))
