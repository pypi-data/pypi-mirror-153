#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from os import environ
from stqe.host.lsm import yield_lsm_config


def target_ports_success():
    errors = []
    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)
        atomic_run("Using LSM to list TARGET_PORTS with protocol %s" % config['protocol'],
                   command=lsm.list,
                   lsm_type="TARGET_PORTS",
                   errors=errors)
        arguments = [
            {'sys': 'false_id'},
            {'tgt': 'false_id'}
        ]
        for argument in arguments:
            atomic_run("Using LSM to list TARGET_PORTS with protocol %s" % config['protocol'],
                       command=lsm.list,
                       lsm_type="TARGET_PORTS",
                       errors=errors,
                       **argument)
    return errors


def target_ports_fail():
    errors = []
    arguments = [
        {'pool': 'false_id'},
        {'vol': 'false_id'},
        {'disk': 'false_id'},
        {'ag': 'false_id'},
        {'fs': 'false_id'},
        {'nfs_export': 'false_id'}
    ]
    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)
        for argument in arguments:
            atomic_run("Trying to fail using LSM to list TARGET_PORTS with protocol %s" % config['protocol'],
                       errors=errors,
                       command=lsm.list,
                       lsm_type="TARGET_PORTS",
                       success=False,
                       expected_ret=2,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = target_ports_success()
    if int(environ['fmf_tier']) == 2:
        errs = target_ports_fail()
    exit(parse_ret(errs))
