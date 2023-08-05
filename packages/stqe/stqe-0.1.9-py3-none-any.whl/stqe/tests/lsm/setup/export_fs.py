#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.lsm import yield_lsm_config
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, write_var
from os import environ


def export_fs():
    print("INFO: Creating snapshot of FS.")
    errors = []

    export_path = environ['fmf_fs_export_path']
    rw_host = environ['fmf_rw_host']
    fs_id = read_var("LSM_FS_ID")

    lsm = LibStorageMgmt(disable_check=True, **list(yield_lsm_config())[0])

    ret, data = atomic_run("Exporting FS '%s'" % fs_id,
                           command=lsm.fs_export,
                           export_path=export_path,
                           rw_host=rw_host,
                           fs=fs_id,
                           return_output=True,
                           errors=errors)

    for line in data.splitlines():
        if export_path in line:
            export_id = line.split()[0].strip()
            atomic_run("Writing var LSM_EXPORT_ID",
                       command=write_var,
                       var={"LSM_EXPORT_ID": export_id},
                       errors=errors)

    return errors


if __name__ == "__main__":
    errs = export_fs()
    exit(parse_ret(errs))
