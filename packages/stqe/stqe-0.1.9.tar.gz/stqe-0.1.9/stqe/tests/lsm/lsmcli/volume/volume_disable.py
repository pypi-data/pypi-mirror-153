#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def volume_disable_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail disabling volume without any paramethers with protocol %s"
                        % config['protocol'], 'command': lsm.volume_disable},
            {'message': "Trying to fail disabling volume with wrong volume with protocol %s"
                        % config['protocol'], 'vol': "WRONG", 'command': lsm.volume_disable}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def volume_disable_no_state_change():
    errors = []

    vol_id = read_var("LSM_VOL_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Disabling volume %s with protocol %s." %
                        (vol_id, config['protocol']), 'vol': vol_id, 'command': lsm.volume_disable},
            {'message': "Disabling volume %s to hit NO_STATE_CHANGE with protocol %s." %
                        (vol_id, config['protocol']), 'vol': vol_id, 'command': lsm.volume_disable, 'expected_ret': 4},
            {'message': "Enabling disabled volume %s with protocol %s." %
                        (vol_id, config['protocol']), 'vol': vol_id, 'command': lsm.volume_enable}
        ]
        for argument in arguments:
            if "expected_ret" not in argument:
                argument['expected_ret'] = 0
            atomic_run(errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 2:
        errs = volume_disable_fail()
        errs + volume_disable_no_state_change()
    exit(parse_ret(errs))
