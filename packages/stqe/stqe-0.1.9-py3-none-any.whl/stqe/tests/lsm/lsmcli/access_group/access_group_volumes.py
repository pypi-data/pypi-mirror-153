#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def access_group_volumes_success():
    errors = []

    ag_id = read_var("LSM_AG_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Listing volumes with access from AG %s with protocol %s." % (ag_id, config['protocol']),
                   command=lsm.access_group_volumes,
                   ag=ag_id,
                   errors=errors)

    return errors


def access_group_volumes_fail():
    errors = []

    ag_name = read_var("LSM_AG_NAME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail listing volumes with access from AG without any paramethers "
                        "with protocol %s" % config['protocol'], 'command': lsm.access_group_volumes},
            {'message': "Trying to fail listing volumes with access from AG with AG NONEXISTENT with protocol %s" % config[
                'protocol'], 'command': lsm.access_group_volumes, 'ag': "NONEXISTENT"},
            {'message': "Trying to fail listing volumes with access from with AG name instead of ID with protocol %s" %
                        config['protocol'], 'command': lsm.access_group_volumes, 'ag': ag_name}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = access_group_volumes_success()
    if int(environ['fmf_tier']) == 2:
        errs = access_group_volumes_fail()
    exit(parse_ret(errs))
