#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def volume_replicate_range_block_size_success():
    errors = []

    sys = read_var("LSM_SYS_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Getting replication block size of sys %s with protocol %s." %
                   (sys, config['protocol']),
                   command=lsm.volume_replicate_range_block_size,
                   sys=sys,
                   errors=errors)
    return errors


def volume_replicate_range_block_size_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail getting replication block size without any paramethers with protocol %s" %
                        config['protocol'], 'command': lsm.volume_replicate_range_block_size},
            {'message': "Trying to fail getting replication block size with WRONG system with protocol %s" %
                        config['protocol'], 'sys': "WRONG", 'command': lsm.volume_replicate_range_block_size}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = volume_replicate_range_block_size_success()
    if int(environ['fmf_tier']) == 2:
        errs = volume_replicate_range_block_size_fail()
    exit(parse_ret(errs))
