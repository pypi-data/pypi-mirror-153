#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


# fs_snap_delete_success is part of fs_snap_create_success() in this same directory


def fs_snap_delete_fail():
    errors = []

    snap_name = read_var("LSM_FS_SNAP_NAME")
    snap_id = read_var("LSM_FS_SNAP_ID")
    fs_id = read_var("LSM_FS_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail deleting snapshot on FS without any paramethers with protocol %s"
                        % config['protocol'], 'command': lsm.fs_snap_delete},
            {'message': "Trying to fail deleting snapshot on FS without 'fs' with protocol %s" % config['protocol'],
             'command': lsm.fs_snap_delete, 'snap': snap_id},
            {'message': "Trying to fail deleting snapshot on FS without 'snap' with protocol %s" % config['protocol'],
             'command': lsm.fs_snap_delete, 'fs': fs_id},
            {'message': "Trying to fail deleting snapshot on FS by using snap name instead of fs-ID with protocol %s"
                        % config['protocol'], 'command': lsm.fs_snap_delete, 'fs': fs_id, 'snap': snap_name},
            {'message': "Trying to fail deleting snapshot on NONEXISTENT FS with protocol %s" % config['protocol'],
             'command': lsm.fs_snap_delete, 'fs': "NONEXISTENT", 'snap': snap_id},
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 2:
        errs = fs_snap_delete_fail()
    exit(parse_ret(errs))
