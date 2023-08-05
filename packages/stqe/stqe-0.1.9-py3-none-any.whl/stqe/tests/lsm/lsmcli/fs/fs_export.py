#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def fs_export_success():
    errors = []

    fs_id = read_var("LSM_FS_ID")
    export_path = read_var("LSM_FS_EXPORT_PATH")
    rw_host = read_var("LSM_RW_HOST")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        ret, data = atomic_run("Exporting FS '%s'" % fs_id,
                               command=lsm.fs_export,
                               export_path=export_path,
                               rw_host=rw_host,
                               fs=fs_id,
                               return_output=True,
                               errors=errors)
        export_id = [line.split()[0].strip() for line in data.splitlines() if export_path in line][0]
        atomic_run("Removing export %s with protocol %s." % (export_id, config['protocol']),
                   command=lsm.fs_unexport,
                   export=export_id,
                   force=True,
                   errors=errors)

        # FIXME: Add more paramethers

    return errors


def fs_export_fail():
    errors = []

    fs_name = read_var("LSM_FS_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail exporting FS without any paramethers with protocol %s" % config['protocol'],
             'command': lsm.fs_export},
            {'message': "Trying to fail exporting FS with wrong 'fs' 'wrong' with protocol %s" % config['protocol'],
             'command': lsm.fs_export, 'fs': "wrong"},
            {'message': "Trying to fail exporting FS with 'fs' name instead of ID with protocol %s" % config[
                'protocol'], 'command': lsm.fs_export, 'fs': fs_name},
        ]

        for argument in arguments:
            if argument['command'] == lsm.fs_export:
                argument['expected_ret'] = 2
            atomic_run(errors=errors,
                       return_output=True,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = fs_export_success()
    if int(environ['fmf_tier']) == 2:
        errs = fs_export_fail()
    exit(parse_ret(errs))
