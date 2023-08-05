#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.vdo import VDO
from libsan.host.fio import fio_stress
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var
from os import environ
from stqe.host.vdo import is_block_device


def xfs_stress():
    errors = []
    vdo = VDO(disable_check=True)

    fs_dir = read_var("FS_DIR")
    vdo_name = environ['fmf_vdo_name']

    ret = is_block_device("/dev/mapper/%s" % vdo_name)
    if ret != True:
        errors.append(ret)
        return errors

    arguments = [
        {'message': "Checking vdo status to get info on data.", 'command': vdo.status, 'name': vdo_name},
        {'message': "Starting fio stress on FS on VDO",
         'command': fio_stress,
         'of': "%s/test.img" % fs_dir,
         'verbose': True,
         # fio settings
         'ioengine': environ['fmf_ioengine'],
         'direct': environ['fmf_direct'],
         'group_reporting': environ['fmf_group_reporting'],
         'bs': environ['fmf_bs'],
         'iodepth': environ['fmf_iodepth'],
         'numjobs': environ['fmf_numjobs'],
         'rw': environ['fmf_rw'],
         'rwmixread': environ['fmf_rwmixread'],
         'randrepeat': environ['fmf_randrepeat'],
         'norandommap': environ['fmf_norandommap'],
         'size': environ['fmf_size'],
         'runtime': int(environ['fmf_runtime'])*60},
        {'message': "Checking vdo status to get info on data.", 'command': vdo.status, 'name': vdo_name}
    ]

    for argument in arguments:
        atomic_run(errors=errors,
                   **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = xfs_stress()
    exit(parse_ret(errs))
