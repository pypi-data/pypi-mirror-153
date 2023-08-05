#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.lsm import yield_lsm_config
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, write_var
from os import environ


def create_volume():
    print("INFO: Creating volume.")
    errors = []

    id = ""
    if 'fmf_id' in environ:
        id = "_" + environ['fmf_id']

    vol_name = read_var("LSM_VOL_NAME" + id)
    vol_size = environ['fmf_vol_size' + id]
    pool_id = read_var("LSM_POOL_ID_VOLUME")

    lsm = LibStorageMgmt(disable_check=True, **list(yield_lsm_config())[0])

    ret, data = atomic_run("Creating volume %s" % vol_name,
                           command=lsm.volume_create,
                           name=vol_name,
                           size=vol_size,
                           pool=pool_id,
                           return_output=True,
                           errors=errors)

    for line in data.splitlines():
        if vol_name in line:
            vol_id = line.split()[0].strip()
            atomic_run("Writing var LSM_VOL_ID",
                       command=write_var,
                       var={"LSM_VOL_ID" + id: vol_id},
                       errors=errors)

    atomic_run("Writing var LSM_VOL_SIZE" + id,
               command=write_var,
               var={"LSM_VOL_SIZE" + id: vol_size},
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = create_volume()
    exit(parse_ret(errs))
