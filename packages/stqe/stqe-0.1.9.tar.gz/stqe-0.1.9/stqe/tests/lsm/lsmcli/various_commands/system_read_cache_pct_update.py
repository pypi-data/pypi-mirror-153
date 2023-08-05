#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config, get_data_from_script_output
from os import environ
from stqe.host.persistent_vars import read_var


def system_read_cache_pct_update_success():
    errors = []

    sys = read_var("LSM_SYS_ID")

    read_pct = int(read_var("LSM_SYSTEM_READ_PCT"))

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        ret, data = atomic_run("Listing systems to backup read percentage",
                               command=lsm.list,
                               lsm_type="SYSTEMS",
                               return_output=True,
                               script=True,
                               errors=errors)
        pct_before = get_data_from_script_output(data)[sys]['Read Cache Percentage']

        atomic_run("Changing system read pct to %s with protocol %s" % (read_pct, config['protocol']),
                   command=lsm.system_read_cache_pct_update,
                   sys=sys,
                   read_pct=read_pct,
                   errors=errors)

        ret, data = atomic_run("Listing systems to check updated read percentage",
                               command=lsm.list,
                               lsm_type="SYSTEMS",
                               return_output=True,
                               script=True,
                               errors=errors)
        pct_after = int(get_data_from_script_output(data)[sys]['Read Cache Percentage'])
        if pct_after != read_pct:
            msg = "FAIL: System cache read percentage did not change, should be %s, got %s" % (read_pct, pct_after)
            print(msg)
            errors.append(msg)

        atomic_run("Returning system read pct to former value with protocol %s" % config['protocol'],
                   command=lsm.system_read_cache_pct_update,
                   sys=sys,
                   read_pct=pct_before,
                   errors=errors)

    return errors


def system_read_cache_pct_update_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail changing system read pct without path with protocol %s" % config['protocol'],
             'command': lsm.system_read_cache_pct_update},
            {'message': "Trying to fail changing system read pct with wrong system with protocol %s" %
                        config['protocol'], 'command': lsm.system_read_cache_pct_update, 'sys': "WRONG"}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = system_read_cache_pct_update_success()
    if int(environ['fmf_tier']) == 2:
        errs = system_read_cache_pct_update_fail()
    exit(parse_ret(errs))
