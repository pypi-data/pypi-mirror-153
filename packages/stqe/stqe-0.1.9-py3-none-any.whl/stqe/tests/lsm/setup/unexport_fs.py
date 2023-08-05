#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.lsm import yield_lsm_config
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, clean_var
from os import environ


def unexport_fs():
    print("INFO: Removing snapshot from FS.")
    errors = []

    var_name = "LSM_" + environ["fmf_export_id"]
    export_id = read_var(var_name)

    lsm = LibStorageMgmt(disable_check=True, **list(yield_lsm_config())[0])

    atomic_run("Unexporting export ID '%s'" % export_id,
               command=lsm.fs_unexport,
               export=export_id,
               force=True,
               errors=errors)

    atomic_run("Removing var %s" % var_name,
               command=clean_var,
               var=var_name,
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = unexport_fs()
    exit(parse_ret(errs))
