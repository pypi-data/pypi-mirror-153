#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def pool_member_info_success():
    errors = []

    pool = read_var("LSM_POOL_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)
        atomic_run("Getting pool member info of pool %s with protocol %s" % (pool, config['protocol']),
                   command=lsm.pool_member_info,
                   pool=pool,
                   errors=errors)
    return errors


def pool_member_info_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail getting pool member info of pool without any paramethers with protocol %s" %
                        config['protocol'], 'command': lsm.pool_member_info},
            {'message': "Trying to fail getting pool member info of pool with WRONG pool with protocol %s" %
                        config['protocol'], 'pool': "WRONG", 'command': lsm.pool_member_info}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = pool_member_info_success()
    if int(environ['fmf_tier']) == 2:
        errs = pool_member_info_fail()
    exit(parse_ret(errs))
