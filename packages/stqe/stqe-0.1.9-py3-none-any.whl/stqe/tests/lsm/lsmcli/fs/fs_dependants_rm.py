#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def fs_dependants_rm_success():
    errors = []

    fs_id = read_var("LSM_FS_ID")
    fs_cloned_name = read_var("LSM_FS_CLONED_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        ret, data = atomic_run("Cloning FS %s to FS %s." % (fs_id, fs_cloned_name),
                               command=lsm.fs_clone,
                               src_fs=fs_id,
                               dst_name=fs_cloned_name,
                               return_output=True,
                               errors=errors)
        fs_cloned_id = [line.split()[0].strip() for line in data.splitlines() if fs_cloned_name in line][0]

        atomic_run("Removing dependants of FS %s with protocol %s." % (fs_id, config['protocol']),
                   command=lsm.fs_dependants_rm,
                   fs=fs_id,
                   errors=errors)

        # this should return 'False', because we just removed the dependant
        ret, data = atomic_run("Checking dependants of FS %s with protocol %s." % (fs_id, config['protocol']),
                               command=lsm.fs_dependants,
                               fs=fs_id,
                               return_output=True,
                               errors=errors)
        if data != "False":
            errors.append("Removing dependants of FS %s did not return 'False', but %s."
                          " Dependants did not get removed." % (fs_id, data))

        # FIXME: Add removing dependants for file

        atomic_run("Removing cloned FS %s with protocol %s." % (fs_cloned_name, config['protocol']),
                   command=lsm.fs_delete,
                   fs=fs_cloned_id,
                   force=True,
                   errors=errors)

    return errors


def fs_dependants_rm_fail():
    errors = []

    fs_name = read_var("LSM_FS_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail removing dependants without any paramethers with protocol %s" % config['protocol'],
             'command': lsm.fs_dependants_rm},
            {'message': "Trying to fail removing dependants FS with wrong 'fs' 'wrong' with protocol %s" % config['protocol'],
             'command': lsm.fs_dependants_rm, 'fs': "wrong"},
            {'message': "Trying to fail removing dependants FS with 'fs' name instead of ID with protocol %s" % config['protocol'],
             'command': lsm.fs_dependants_rm, 'fs': fs_name},
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def fs_dependants_rm_fail_no_state_change():
    errors = []

    fs_id = read_var("LSM_FS_ID")
    fs_cloned_name = read_var("LSM_FS_CLONED_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Removing dependants of FS %s with protocol %s to hit NO_STATE_CHANGE." % (fs_id, config['protocol']),
                   command=lsm.fs_dependants_rm,
                   fs=fs_id,
                   expected_ret=4,
                   errors=errors)

        ret, data = atomic_run("Cloning FS %s to FS %s." % (fs_id, fs_cloned_name),
                               command=lsm.fs_clone,
                               src_fs=fs_id,
                               dst_name=fs_cloned_name,
                               return_output=True,
                               errors=errors)
        fs_cloned_id = [line.split()[0].strip() for line in data.splitlines() if fs_cloned_name in line][0]

        atomic_run("Removing dependants of FS %s with protocol %s." % (fs_id, config['protocol']),
                   command=lsm.fs_dependants_rm,
                   fs=fs_id,
                   errors=errors)

        atomic_run("Removing cloned FS %s with protocol %s." % (fs_cloned_name, config['protocol']),
                   command=lsm.fs_delete,
                   fs=fs_cloned_id,
                   force=True,
                   errors=errors)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = fs_dependants_rm_success()
    if int(environ['fmf_tier']) == 2:
        errs = fs_dependants_rm_fail()
        errs += fs_dependants_rm_fail_no_state_change()
    exit(parse_ret(errs))
