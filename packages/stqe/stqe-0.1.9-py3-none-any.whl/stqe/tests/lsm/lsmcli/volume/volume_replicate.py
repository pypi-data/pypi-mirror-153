#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def volume_replicate_success():
    errors = []

    vol_id = read_var("LSM_VOL_ID")
    rep_name = read_var("LSM_VOL_REP_NAME")
    pool_id = read_var("LSM_POOL_ID_VOLUME")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        # TODO: Replicate to different pool
        rep_types = ["CLONE", "COPY", "MIRROR_ASYNC", "MIRROR_SYNC"]
        if 'ontap' in config['protocol']:
            rep_types = ["CLONE"]  # only clone is supported on ontap yet


        for rep_type in rep_types:
            ret, data = atomic_run("Replicating volume %s to %s with type %s with protocol %s." %
                                   (vol_id, rep_name, rep_type, config['protocol']),
                                   command=lsm.volume_replicate,
                                   name=rep_name,
                                   vol=vol_id,
                                   pool=pool_id,
                                   rep_type=rep_type,
                                   return_output=True,
                                   errors=errors)
            rep_id = [line.split()[0].strip() for line in data.splitlines() if rep_name in line][0]
            atomic_run("Removing volume %s with protocol %s." % (rep_name, config['protocol']),
                       command=lsm.volume_delete,
                       vol=rep_id,
                       force=True,
                       errors=errors)
    return errors


def volume_replicate_fail():
    errors = []

    vol_id = read_var("LSM_VOL_ID")
    rep_name = read_var("LSM_VOL_REP_NAME")
    rep_type = "CLONE"

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail replicating volume without any paramethers with protocol %s" %
                        config['protocol'], 'command': lsm.volume_replicate},
            {'message': "Trying to fail replicating volume without volume with protocol %s" %
                        config['protocol'], 'name': rep_name, 'rep_type': rep_type, 'command': lsm.volume_replicate},
            {'message': "Trying to fail replicating volume without name with protocol %s" %
                        config['protocol'], 'vol': vol_id, 'rep_type': rep_type, 'command': lsm.volume_replicate},
            {'message': "Trying to fail replicating volume without rep-type with protocol %s" %
                        config['protocol'], 'vol': vol_id, 'name': rep_name, 'command': lsm.volume_replicate},
            {'message': "Trying to fail replicating volume with wrong volume with protocol %s" %
                        config['protocol'], 'name': rep_name, 'rep_type': rep_type, 'vol': "WRONG",
             'command': lsm.volume_replicate},
            {'message': "Trying to fail replicating volume with wrong type with protocol %s" %
                        config['protocol'], 'name': rep_name, 'rep_type': "WRONG", 'vol': vol_id,
             'command': lsm.volume_replicate},
            {'message': "Trying to fail replicating volume with wrong pool with protocol %s" %
                        config['protocol'], 'name': rep_name, 'rep_type': rep_type, 'vol': vol_id, 'pool': "WRONG",
             'command': lsm.volume_replicate},
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def volume_replicate_name_conflict():
    errors = []

    vol_id = read_var("LSM_VOL_ID")
    rep_name = read_var("LSM_VOL_NAME")
    pool_id = read_var("LSM_POOL_ID_VOLUME")
    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)
        for rep_type in ["CLONE", "COPY", "MIRROR_ASYNC", "MIRROR_SYNC"]:
            atomic_run("Replicating volume %s to %s with type %s to hit NAME_CONFLICT with protocol %s." %
                       (vol_id, rep_name, rep_type, config['protocol']),
                       command=lsm.volume_replicate,
                       name=rep_name,
                       vol=vol_id,
                       pool=pool_id,
                       rep_type=rep_type,
                       return_output=True,
                       expected_ret=4,
                       errors=errors)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = volume_replicate_success()
    if int(environ['fmf_tier']) == 2:
        errs = volume_replicate_fail()
        errs += volume_replicate_name_conflict()
    exit(parse_ret(errs))
