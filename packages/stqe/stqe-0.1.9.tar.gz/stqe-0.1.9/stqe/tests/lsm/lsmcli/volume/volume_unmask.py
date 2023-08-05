#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def volume_unmask_fail():
    errors = []

    vol_id = read_var("LSM_VOL_ID")
    ag_id = read_var("LSM_AG_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail unmasking access group to volume without any paramethers with protocol %s"
                        % config['protocol'], 'command': lsm.volume_unmask},
            {'message': "Trying to fail unmasking access group to volume without volume with protocol %s"
                        % config['protocol'], 'ag': ag_id, 'command': lsm.volume_unmask},
            {'message': "Trying to fail unmasking access group to volume without access group with protocol %s"
                        % config['protocol'], 'vol': vol_id, 'command': lsm.volume_unmask},
            {'message': "Trying to fail unmasking access group to volume with wrong volume with protocol %s"
                        % config['protocol'], 'ag': ag_id, 'vol': "WRONG", 'command': lsm.volume_unmask},
            {'message': "Trying to fail unmasking access group to volume with wrong access group with protocol %s"
                        % config['protocol'], 'vol': vol_id, 'ag': "WRONG", 'command': lsm.volume_unmask}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def volume_unmask_no_state_change():
    errors = []

    vol_id = read_var("LSM_VOL_ID")
    ag_id = read_var("LSM_AG_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Removing access for access group %s to volume %s to hit NO_STATE_CHANGE with protocol %s." %
                        (ag_id, vol_id, config['protocol']), 'vol': vol_id, 'ag': ag_id, 'command': lsm.volume_unmask}
        ]
        for argument in arguments:
            atomic_run(expected_ret=4,
                       errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 2:
        errs = volume_unmask_fail()
        errs + volume_unmask_no_state_change()
    exit(parse_ret(errs))
