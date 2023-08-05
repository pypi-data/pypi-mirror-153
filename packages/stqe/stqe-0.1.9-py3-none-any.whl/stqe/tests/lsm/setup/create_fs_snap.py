#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.lsm import yield_lsm_config
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, write_var
from os import environ


def create_fs():
    print("INFO: Creating snapshot of FS.")
    errors = []

    snap_name = environ['fmf_fs_snap_name']
    fs_id = read_var("LSM_FS_ID")

    lsm = LibStorageMgmt(disable_check=True, **list(yield_lsm_config())[0])

    ret, data = atomic_run("Creating snapshot of FS '%s'" % fs_id,
                           command=lsm.fs_snap_create,
                           name=snap_name,
                           fs=fs_id,
                           return_output=True,
                           errors=errors)

    for line in data.splitlines():
        if snap_name in line:
            fs_snap_id = line.split()[0].strip()
            atomic_run("Writing var LSM_FS_ID",
                       command=write_var,
                       var={"LSM_FS_SNAP_ID": fs_snap_id},
                       errors=errors)

    return errors


if __name__ == "__main__":
    errs = create_fs()
    exit(parse_ret(errs))
