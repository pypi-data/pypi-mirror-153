#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def volume_phy_disk_cache_update_success():
    errors = []

    vol = read_var("LSM_VOL_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        ret, data = atomic_run("Getting read cache policy of volume %s." % vol,
                               command=lsm.volume_cache_info,
                               vol=vol,
                               return_output=True,
                               script=True,
                               errors=errors)
        old_policy = None
        for line in data.splitlines():
            if "Physical Disk Cache" in line:
                old_policy = line.split().pop().strip()[:-1]  # policy is 'disabled' but cli takes 'disable'

        for policy in ["enable", "disable", "Enable", "Disable", "ENABLE", "DISABLE"]:
            atomic_run("Updating policy of volume %s to be %s with protocol %s." % (vol, policy, config['protocol']),
                       command=lsm.volume_phy_disk_cache_update,
                       vol=vol,
                       policy=policy,
                       errors=errors)

        atomic_run("Returning policy of volume %s to former state '%s' with protocol %s." %
                   (vol, old_policy, config['protocol']),
                   command=lsm.volume_phy_disk_cache_update,
                   vol=vol,
                   policy=old_policy,
                   errors=errors)
    return errors


def volume_phy_disk_cache_update_fail():
    errors = []

    vol = read_var("LSM_VOL_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail changing physical disk cache without any paramethers with protocol %s" %
                        config['protocol'], 'command': lsm.volume_phy_disk_cache_update},
            {'message': "Trying to fail changing  physical disk cache with WRONG volume with protocol %s" %
                        config['protocol'], 'vol': "WRONG", 'policy': "enable",
             'command': lsm.volume_phy_disk_cache_update},
            {'message': "Trying to fail changing  physical disk cache with WRONG policy with protocol %s" %
                        config['protocol'], 'vol': vol, 'policy': "WRONG",
             'command': lsm.volume_phy_disk_cache_update}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def volume_phy_disk_cache_update_offline():
    errors = []
    # TODO: Check updating policy of offline volume, create test
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = volume_phy_disk_cache_update_success()
    if int(environ['fmf_tier']) == 2:
        errs = volume_phy_disk_cache_update_fail()
    exit(parse_ret(errs))
