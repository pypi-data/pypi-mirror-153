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

    var_fs_id = "LSM_" + environ["fmf_fs_id"]
    fs_id = read_var(var_fs_id)
    clone_name = environ["fmf_fs_cloned_name"]

    lsm = LibStorageMgmt(disable_check=True, **list(yield_lsm_config())[0])

    ret, data = atomic_run("Cloning FS %s to FS %s." % (fs_id, clone_name),
                           command=lsm.fs_clone,
                           src_fs=fs_id,
                           dst_name=clone_name,
                           return_output=True,
                           errors=errors)
    cloned_fs_id = [line.split()[0].strip() for line in data.splitlines() if clone_name in line][0]

    atomic_run("Writing var LSM_FS_CLONED_ID",
               command=write_var,
               var={"LSM_FS_CLONED_ID": cloned_fs_id},
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = create_fs()
    exit(parse_ret(errs))
