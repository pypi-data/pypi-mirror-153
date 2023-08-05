#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def fs_snap_restore_success():
    errors = []

    snap_id = read_var("LSM_FS_SNAP_ID")
    fs_id = read_var("LSM_FS_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Restoring FS %s from snapshot %s with protocol %s." % (fs_id, snap_id, config['protocol']),
                   command=lsm.fs_snap_restore,
                   fs=fs_id,
                   snap=snap_id,
                   force=True,
                   errors=errors)
        # FIXME: Add test with 'lsm_file' and 'fileas'
    return errors


def fs_snap_restore_fail():
    errors = []

    fs_id = read_var("LSM_FS_ID")
    snap_id = read_var("LSM_FS_SNAP_ID")
    snap_name = read_var("LSM_FS_SNAP_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail restoring FS from snapshot without any paramethers with protocol %s" % config[
                'protocol'], 'command': lsm.fs_snap_restore},
            {'message': "Trying to fail restoring FS from snapshot without 'snap' with protocol %s" % config[
                'protocol'], 'command': lsm.fs_snap_restore, 'fs': fs_id},
            {'message': "Trying to fail restoring FS from snapshot without 'fs' with protocol %s" % config[
                'protocol'], 'command': lsm.fs_snap_restore, 'snap': snap_id},
            {'message': "Trying to fail restoring FS from snapshot with wrong 'snap' with protocol %s" %
                        config['protocol'], 'command': lsm.fs_snap_restore, 'fs': fs_id, 'snap': "wrong"},
            {'message': "Trying to fail restoring FS from snapshot with wrong 'fs' with protocol %s" %
                        config['protocol'], 'command': lsm.fs_snap_restore, 'fs': "wrong", 'snap': snap_id},
            {'message': "Trying to fail restoring FS from snapshot by giving 'snap' name "
                        "instead of ID with protocol %s" % config['protocol'],
             'command': lsm.fs_snap_restore, 'snap': snap_name, 'fs': fs_id},
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = fs_snap_restore_success()
    if int(environ['fmf_tier']) == 2:
        errs = fs_snap_restore_fail()
    exit(parse_ret(errs))
