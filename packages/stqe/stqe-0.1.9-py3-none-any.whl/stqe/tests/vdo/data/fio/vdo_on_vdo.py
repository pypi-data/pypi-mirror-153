#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.vdo import VDO
from libsan.host.fio import fio_stress
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var
from os import environ
from stqe.host.vdo import is_block_device
from stqe.host.vdo import minimum_slab_size


def vdo_on_vdo_stress():
    errors = []
    vdo = VDO(disable_check=True)

    device = read_var("VDO_DEVICE")
    vdo_name = environ['fmf_vdo_name']

    ret = is_block_device("/dev/mapper/%s" % vdo_name)
    if ret != True:
        errors.append(ret)
        print(ret)
        return errors
    vdo_name = vdo_name + "_on_vdo"

    arguments = [
        {'message': "Creating VDO device on %s" % device, 'command': vdo.create, 'name': vdo_name, 'device': device},
        {'message': "Checking vdo status to get info on data.", 'command': vdo.status, 'name': vdo_name},
        {'message': "Starting fio stress on VDO on VDO",
         'command': fio_stress,
         'of': "/dev/mapper/%s" % vdo_name,
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
        {'message': "Checking vdo status to get info on data.", 'command': vdo.status, 'name': vdo_name},
        {'message': "Removing VDO on VDO", "command": vdo.remove, 'name': vdo_name}
    ]


    min_slab_size = minimum_slab_size(device)
    if min_slab_size is not None:
        arguments[0]['slab_size'] = min_slab_size

    for argument in arguments:
        atomic_run(errors=errors,
                   **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 2:
        errs = vdo_on_vdo_stress()
    exit(parse_ret(errs))
