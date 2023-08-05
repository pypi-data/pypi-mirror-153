#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def fs_dependants_success():
    errors = []

    fs_id = read_var("LSM_FS_ID")
    fs_cloned_id = read_var("LSM_FS_CLONED_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        # this should return 'True', because this FS has dependant - cloned FS
        ret, data = atomic_run("Checking dependants of FS %s with protocol %s." % (fs_id, config['protocol']),
                               command=lsm.fs_dependants,
                               fs=fs_id,
                               return_output=True,
                               errors=errors)
        if data != "True":
            errors.append("Checking dependants on FS %s did not return data 'True', but %s" % (fs_id, data))

        # this should return 'False', because this is the cloned FS without dependants
        ret, data = atomic_run("Checking dependants of FS %s with protocol %s." % (fs_cloned_id, config['protocol']),
                               command=lsm.fs_dependants,
                               fs=fs_cloned_id,
                               return_output=True,
                               errors=errors)
        if data != "False":
            errors.append("Checking dependants on FS %s did not return data 'False', but %s" % (fs_cloned_id, data))

        # FIXME: Add checking dependants for file
        # FIXME: Add tests with snapshots as dependants
    return errors


def fs_dependants_fail():
    errors = []

    fs_name = read_var("LSM_FS_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail checking dependants without any paramethers with protocol %s" % config['protocol'],
             'command': lsm.fs_dependants},
            {'message': "Trying to fail checking dependants FS with wrong 'fs' 'wrong' with protocol %s" % config['protocol'],
             'command': lsm.fs_dependants, 'fs': "wrong"},
            {'message': "Trying to fail checking dependants FS with 'fs' name instead of ID with protocol %s" % config['protocol'],
             'command': lsm.fs_dependants, 'fs': fs_name},
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = fs_dependants_success()
    if int(environ['fmf_tier']) == 2:
        errs = fs_dependants_fail()
    exit(parse_ret(errs))
