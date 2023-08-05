#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def fs_resize_success():
    errors = []

    fs_id = read_var("LSM_FS_ID")
    old_fs_size = read_var("LSM_FS_SIZE")
    new_fs_size = environ['fmf_new_fs_size']

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Resizing FS %s to size %s with protocol %s." % (fs_id, new_fs_size, config['protocol']),
                   command=lsm.fs_resize,
                   fs=fs_id,
                   size=new_fs_size,
                   force=True,
                   errors=errors)

        # FIXME: Check the size is changed.

        atomic_run("Resizing FS %s back to size %s with protocol %s." % (fs_id, old_fs_size, config['protocol']),
                   command=lsm.fs_resize,
                   fs=fs_id,
                   size=old_fs_size,
                   force=True,
                   errors=errors)

    return errors


def fs_resize_fail():
    errors = []

    fs_id = read_var("LSM_FS_ID")
    fs_name = read_var("LSM_FS_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail resizing without any paramethers with protocol %s" % config['protocol'],
             'command': lsm.fs_resize},
            {'message': "Trying to fail resizing FS with wrong 'fs' 'wrong' with protocol %s" % config['protocol'],
             'command': lsm.fs_resize, 'fs': "wrong"},
            {'message': "Trying to fail resizing FS with 'fs' name instead of ID with protocol %s" % config['protocol'],
             'command': lsm.fs_resize, 'fs': fs_name},
            {'message': "Trying to fail resizing FS without 'size' with protocol %s" % config['protocol'],
             'command': lsm.fs_resize, 'fs': fs_id},
            {'message': "Trying to fail resizing FS without 'fs' with protocol %s" % config['protocol'],
             'command': lsm.fs_resize, 'size': 10},
            {'message': "Trying to fail resizing FS with 'size' '-1' with protocol %s" % config['protocol'],
             'command': lsm.fs_resize, 'fs': fs_id, 'size': -1},
            {'message': "Trying to fail resizing FS with 'size' '0' with protocol %s" % config['protocol'],
             'command': lsm.fs_resize, 'fs': fs_id, 'size': 0},
            {'message': "Trying to fail resizing FS with 'size' 'B' with protocol %s" % config['protocol'],
             'command': lsm.fs_resize, 'fs': fs_id, 'size': "B"}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       force=True,
                       **argument)
    return errors


def fs_resize_fail_not_enough_space():
    errors = []

    fs_id = read_var("LSM_FS_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail resizing FS with 'size' '8000P' with protocol %s" % config['protocol'],
             'command': lsm.fs_resize, 'fs': fs_id, 'size': "8000P"}
        ]
        for argument in arguments:
            atomic_run(expected_ret=4,
                       errors=errors,
                       force=True,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = fs_resize_success()
    if int(environ['fmf_tier']) == 2:
        errs = fs_resize_fail()
        errs += fs_resize_fail_not_enough_space()
    exit(parse_ret(errs))
