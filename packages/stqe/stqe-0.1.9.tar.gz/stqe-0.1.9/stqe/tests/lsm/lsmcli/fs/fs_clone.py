#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def fs_clone_success():
    errors = []

    clone_name = read_var("LSM_FS_CLONED_NAME")
    fs_id = read_var("LSM_FS_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        ret, data = atomic_run("Cloning FS %s to FS %s with protocol %s." % (fs_id, clone_name, config['protocol']),
                               command=lsm.fs_clone,
                               src_fs=fs_id,
                               dst_name=clone_name,
                               return_output=True,
                               errors=errors)
        cloned_fs_id = [line.split()[0].strip() for line in data.splitlines() if clone_name in line][0]
        atomic_run("Removing cloned FS %s with protocol %s." % (clone_name, config['protocol']),
                   command=lsm.fs_delete,
                   fs=cloned_fs_id,
                   force=True,
                   errors=errors)
        # FIXME: Add test with backing-snapshot
    return errors


def fs_clone_fail():
    errors = []

    clone_name = read_var("LSM_FS_CLONED_NAME")
    fs_id = read_var("LSM_FS_ID")
    fs_name = read_var("LSM_FS_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail cloning FS without any paramethers with protocol %s" % config['protocol'],
             'command': lsm.fs_clone},
            {'message': "Trying to fail cloning FS without 'dst-name' with protocol %s" % config['protocol'],
             'command': lsm.fs_clone, 'src_fs': fs_id},
            {'message': "Trying to fail cloning FS without 'src-fs' with protocol %s" % config['protocol'],
             'command': lsm.fs_clone, 'dst_name': clone_name},
            {'message': "Trying to fail cloning FS with wrong 'src-fs' 'wrong' with protocol %s" % config['protocol'],
             'command': lsm.fs_clone, 'dst_name': clone_name, 'src_fs': "wrong"},
            {'message': "Trying to fail cloning FS by giving 'src-fs' name instead of ID with protocol %s" % config['protocol'],
             'command': lsm.fs_clone, 'dst_name': clone_name, 'src_fs': fs_name}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def fs_clone_fail_name_conflict():
    errors = []

    clone_name = read_var("LSM_FS_CLONED_NAME")
    fs_id = read_var("LSM_FS_ID")
    fs_name = read_var("LSM_FS_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        ret, data = atomic_run("Cloning FS %s to FS %s with protocol %s." % (fs_id, clone_name, config['protocol']),
                               command=lsm.fs_clone,
                               src_fs=fs_id,
                               dst_name=clone_name,
                               return_output=True,
                               errors=errors)
        cloned_fs_id = [line.split()[0].strip() for line in data.splitlines() if clone_name in line][0]

        atomic_run("Cloning FS %s again to hit NAME CONFLICT with cloned FS name with protocol %s." % (fs_name, config['protocol']),
                   command=lsm.fs_clone,
                   src_fs=fs_id,
                   dst_name=clone_name,
                   return_output=True,
                   expected_ret=4,
                   errors=errors)

        atomic_run("Cloning FS %s again to hit NAME CONFLICT with origin FS name with protocol %s." % (fs_name, config['protocol']),
                   command=lsm.fs_clone,
                   src_fs=fs_id,
                   dst_name=fs_name,
                   return_output=True,
                   expected_ret=4,
                   errors=errors)

        atomic_run("Removing cloned FS %s with protocol %s." % (clone_name, config['protocol']),
                   command=lsm.fs_delete,
                   fs=cloned_fs_id,
                   force=True,
                   errors=errors)
    return errors

if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = fs_clone_success()
    if int(environ['fmf_tier']) == 2:
        errs = fs_clone_fail()
        errs += fs_clone_fail_name_conflict()
    exit(parse_ret(errs))
