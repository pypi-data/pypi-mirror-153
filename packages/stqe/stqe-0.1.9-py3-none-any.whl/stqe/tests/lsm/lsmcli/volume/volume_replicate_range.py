#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def volume_replicate_range_success():
    errors = []

    src_vol = read_var("LSM_VOL_ID")
    dst_vol = read_var("LSM_VOL_ID_2")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        rep_types = ["CLONE", "COPY"]
        if 'ontap' in config['protocol']:
            rep_types = ["CLONE"]  # copy is not supported on ontap yet

        for rep_type in rep_types:
            atomic_run("Replicating volume %s to volume %s with type %s with protocol %s." %
                       (src_vol, dst_vol, rep_type, config['protocol']),
                       command=lsm.volume_replicate_range,
                       src_vol=src_vol,
                       dst_vol=dst_vol,
                       rep_type=rep_type,
                       src_start=0,
                       dst_start=0,
                       count=100,
                       force=True,
                       errors=errors)

            atomic_run("Removing dependency between replicated volumes %s and %s" % (src_vol, dst_vol),
                       command=lsm.volume_dependants_rm,
                       vol=src_vol,
                       errors=errors)

            atomic_run("Replicating volume %s to volume %s with type %s with repeated arguments with protocol %s." %
                       (src_vol, dst_vol, rep_type, config['protocol']),
                       command=lsm.volume_replicate_range,
                       src_vol=src_vol,
                       dst_vol=dst_vol,
                       rep_type=rep_type,
                       src_start=[0, 100, -100],
                       dst_start=[0, 200, -100],
                       count=[100, 1, -100],
                       force=True,
                       errors=errors)

            atomic_run("Removing dependency between replicated volumes %s and %s" % (src_vol, dst_vol),
                       command=lsm.volume_dependants_rm,
                       vol=src_vol,
                       errors=errors)
    return errors


def volume_replicate_range_fail():
    errors = []

    src_vol = read_var("LSM_VOL_ID")
    dst_vol = read_var("LSM_VOL_ID_2")
    rep_type = "CLONE"

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail replicating volume range without any paramethers with protocol %s" %
                        config['protocol'], 'command': lsm.volume_replicate_range},
            {'message': "Trying to fail replicating volume range without source volume with protocol %s" %
                        config['protocol'], 'dst_vol': dst_vol, 'src_start': 0, 'dst_start': 0, 'count': 100,
             'rep_type': rep_type, 'command': lsm.volume_replicate_range},
            {'message': "Trying to fail replicating volume range without destination volume with protocol %s" %
                        config['protocol'], 'src_vol': src_vol, 'src_start': 0, 'dst_start': 0, 'count': 100,
             'rep_type': rep_type, 'command': lsm.volume_replicate_range},
            {'message': "Trying to fail replicating volume range without replication type volume with protocol %s" %
                        config['protocol'], 'src_vol': src_vol, 'src_start': 0, 'dst_start': 0, 'count': 100,
             'dst_vol': dst_vol, 'command': lsm.volume_replicate_range},
            {'message': "Trying to fail replicating volume range without source start with protocol %s" %
                        config['protocol'], 'src_vol': src_vol, 'dst_vol': dst_vol, 'dst_start': 0, 'count': 100,
             'rep_type': rep_type, 'command': lsm.volume_replicate_range},
            {'message': "Trying to fail replicating volume range without destination start with protocol %s" %
                        config['protocol'], 'src_vol': src_vol, 'src_start': 0, 'dst_vol': dst_vol, 'count': 100,
             'rep_type': rep_type, 'command': lsm.volume_replicate_range},
            {'message': "Trying to fail replicating volume range without block count with protocol %s" %
                        config['protocol'], 'src_vol': src_vol, 'src_start': 0, 'dst_start': 0, 'dst_vol': dst_vol,
             'rep_type': rep_type, 'command': lsm.volume_replicate_range},
            {'message': "Trying to fail replicating volume range with wrong source volume with protocol %s" %
                        config['protocol'], 'src_vol': "WRONG", 'dst_vol': dst_vol, 'src_start': 0, 'dst_start': 0,
             'count': 100, 'rep_type': rep_type, 'command': lsm.volume_replicate_range},
            {'message': "Trying to fail replicating volume range with wrong destination volume with protocol %s" %
                        config['protocol'], 'src_vol': src_vol, 'dst_vol': "WRONG", 'src_start': 0, 'dst_start': 0,
             'count': 100, 'rep_type': rep_type, 'command': lsm.volume_replicate_range},
            {'message': "Trying to fail replicating volume range with wrong source start with protocol %s" %
                        config['protocol'], 'src_vol': src_vol, 'dst_vol': dst_vol, 'src_start': "WRONG",
             'dst_start': 0,
             'count': 100, 'rep_type': rep_type, 'command': lsm.volume_replicate_range},
            {'message': "Trying to fail replicating volume range with wrong destination start with protocol %s" %
                        config['protocol'], 'src_vol': src_vol, 'dst_vol': dst_vol, 'src_start': 0,
             'dst_start': "WRONG",
             'count': 100, 'rep_type': rep_type, 'command': lsm.volume_replicate_range},
            {'message': "Trying to fail replicating volume range with wrong block count with protocol %s" %
                        config['protocol'], 'src_vol': src_vol, 'dst_vol': dst_vol, 'src_start': 0, 'dst_start': 0,
             'count': "WRONG", 'rep_type': rep_type, 'command': lsm.volume_replicate_range},
            {'message': "Trying to fail replicating volume range with wrong replication type with protocol %s" %
                        config['protocol'], 'src_vol': src_vol, 'dst_vol': dst_vol, 'src_start': 0, 'dst_start': 0,
             'count': 100, 'rep_type': "WRONG", 'command': lsm.volume_replicate_range}
        ]
        for argument in arguments:
            ret, data = atomic_run(expected_ret=2,
                                   errors=errors,
                                   return_output=True,
                                   **argument)
            if ret == 0:
                atomic_run("Removing dependency between replicated volumes %s and %s after not failing" %
                           (src_vol, dst_vol),
                           command=lsm.volume_dependants_rm,
                           vol=src_vol,
                           errors=errors)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = volume_replicate_range_success()
    if int(environ['fmf_tier']) == 2:
        errs = volume_replicate_range_fail()
    exit(parse_ret(errs))
