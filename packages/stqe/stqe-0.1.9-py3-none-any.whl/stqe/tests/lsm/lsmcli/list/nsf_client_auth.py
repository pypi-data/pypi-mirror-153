#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from os import environ
from stqe.host.lsm import yield_lsm_config


def nsf_client_auth_success():
    errors = []
    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)
        atomic_run("Using LSM to list NFS_CLIENT_AUTH with protocol %s" % config['protocol'],
                   command=lsm.list,
                   lsm_type="NFS_CLIENT_AUTH",
                   errors=errors)
    return errors


def nsf_client_auth_fail():
    errors = []
    arguments = [
        {'sys': 'false_id'},
        {'pool': 'false_id'},
        {'vol': 'false_id'},
        {'disk': 'false_id'},
        {'ag': 'false_id'},
        {'fs': 'false_id'},
        {'nfs_export': 'false_id'},
        {'tgt': 'false_id'}
    ]
    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)
        for argument in arguments:
            atomic_run("Trying to fail using LSM to list NFS_CLIENT_AUTH with protocol %s" % config['protocol'],
                       errors=errors,
                       command=lsm.list,
                       lsm_type="NFS_CLIENT_AUTH",
                       success=False,
                       expected_ret=2,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = nsf_client_auth_success()
    if int(environ['fmf_tier']) == 2:
        errs = nsf_client_auth_fail()
    exit(parse_ret(errs))
