#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def volume_cache_info_success():
    errors = []

    vol = read_var("LSM_VOL_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Getting RAM cache info for volume %s with protocol %s." %
                   (vol, config['protocol']),
                   command=lsm.volume_cache_info,
                   vol=vol,
                   errors=errors)
    return errors


def volume_cache_info_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail getting RAM cache info without any paramethers with protocol %s" %
                        config['protocol'], 'command': lsm.volume_cache_info},
            {'message': "Trying to fail getting RAM cache info with WRONG volume with protocol %s" %
                        config['protocol'], 'vol': "WRONG", 'command': lsm.volume_cache_info}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def volume_cache_info_offline():
    errors = []
    # TODO: Check if one can get RAM cache info for disabled volume, write test for it
    return errors

if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = volume_cache_info_success()
    if int(environ['fmf_tier']) == 2:
        errs = volume_cache_info_fail()
    exit(parse_ret(errs))
