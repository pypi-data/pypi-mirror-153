#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def volume_enable_success():
    errors = []

    vol_id = read_var("LSM_VOL_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Disabling volume %s with protocol %s." % (vol_id, config['protocol']),
                   command=lsm.volume_disable,
                   vol=vol_id,
                   errors=errors)

        atomic_run("Enabling volume %s with protocol %s." % (vol_id, config['protocol']),
                   command=lsm.volume_enable,
                   vol=vol_id,
                   errors=errors)

        return errors


def volume_enable_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail enabling volume without any paramethers with protocol %s"
                        % config['protocol'], 'command': lsm.volume_enable},
            {'message': "Trying to fail enabling volume with wrong volume with protocol %s"
                        % config['protocol'], 'vol': "WRONG", 'command': lsm.volume_enable}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def volume_enable_no_state_change():
    errors = []

    vol_id = read_var("LSM_VOL_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Enabling enabled volume %s to hit NO_STATE_CHANGE with protocol %s." %
                        (vol_id, config['protocol']), 'vol': vol_id, 'command': lsm.volume_enable}
        ]
        for argument in arguments:
            atomic_run(expected_ret=4,
                       errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = volume_enable_success()
    if int(environ['fmf_tier']) == 2:
        errs = volume_enable_fail()
        errs + volume_enable_no_state_change()
    exit(parse_ret(errs))
