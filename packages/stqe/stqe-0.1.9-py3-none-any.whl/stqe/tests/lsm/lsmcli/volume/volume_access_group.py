#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def volume_access_group_success():
    errors = []

    vol_id = read_var("LSM_VOL_ID")
    ag_id = read_var("LSM_AG_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        ret, data = atomic_run("Checking access group for volume %s with protocol %s." % (vol_id, config['protocol']),
                               command=lsm.volume_access_group,
                               vol=vol_id,
                               return_output=True,
                               errors=errors)
        if data is None or ag_id not in data:
            msg = "FAIL: Could not find access group %s link to volume %s" % (ag_id, vol_id)
            print(msg)
            errors.append(msg)
        return errors


def volume_access_group_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail checking access group for volume without any paramethers with protocol %s"
                        % config['protocol'], 'command': lsm.volume_access_group}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = volume_access_group_success()
    if int(environ['fmf_tier']) == 2:
        errs = volume_access_group_fail()
    exit(parse_ret(errs))
