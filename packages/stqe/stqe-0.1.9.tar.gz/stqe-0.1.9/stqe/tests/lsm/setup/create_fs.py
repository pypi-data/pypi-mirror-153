#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.lsm import yield_lsm_config
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, write_var
from os import environ


def create_fs():
    print("INFO: Creating FS.")
    errors = []

    fs_name = read_var("LSM_FS_NAME")
    fs_size = environ['fmf_fs_size']
    pool_id = read_var("LSM_POOL_ID")

    lsm = LibStorageMgmt(disable_check=True, **list(yield_lsm_config())[0])

    ret, data = atomic_run("Creating FS",
                           command=lsm.fs_create,
                           name=fs_name,
                           size=fs_size,
                           pool=pool_id,
                           return_output=True,
                           errors=errors)

    for line in data.splitlines():
        if pool_id in line:
            fs_id = line.split()[0].strip()
            atomic_run("Writing var LSM_FS_ID",
                       command=write_var,
                       var={"LSM_FS_ID": fs_id},
                       errors=errors)

    atomic_run("Writing var LSM_FS_SIZE",
               command=write_var,
               var={"LSM_FS_SIZE": fs_size},
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = create_fs()
    exit(parse_ret(errs))
