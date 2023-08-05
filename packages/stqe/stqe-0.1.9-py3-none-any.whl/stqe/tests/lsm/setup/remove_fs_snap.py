#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.lsm import yield_lsm_config
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, clean_var
from os import environ


def create_fs():
    print("INFO: Removing snapshot from FS.")
    errors = []

    snap_var_name = "LSM_" + environ["fmf_fs_snap_id"]
    fs_snap_id = read_var(snap_var_name)

    fs_id = read_var("LSM_" + environ["fmf_fs_id"])

    lsm = LibStorageMgmt(disable_check=True, **list(yield_lsm_config())[0])

    atomic_run("Removing snapshot %s from FS %s" % (fs_snap_id, fs_id),
               command=lsm.fs_snap_delete,
               snap=fs_snap_id,
               fs=fs_id,
               force=True,
               errors=errors)

    atomic_run("Removing var %s" % snap_var_name,
               command=clean_var,
               var=snap_var_name,
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = create_fs()
    exit(parse_ret(errs))
