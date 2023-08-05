#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from os import environ
from stqe.host.lsm import yield_lsm_config
from stqe.host.persistent_vars import read_var


def snapshots_success():
    errors = []

    fs_id = read_var("LSM_FS_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)
        atomic_run("Using LSM to list SNAPSHOTS with protocol %s" % config['protocol'],
                   command=lsm.list,
                   lsm_type="SNAPSHOTS",
                   fs=fs_id,
                   errors=errors)
        arguments = [
            {'sys': 'false_id'}
        ]
        for argument in arguments:
            atomic_run("Using LSM to list TARGET_PORTS with protocol %s" % config['protocol'],
                       command=lsm.list,
                       lsm_type="TARGET_PORTS",
                       errors=errors,
                       **argument)
    return errors

if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = snapshots_success()
    exit(parse_ret(errs))
