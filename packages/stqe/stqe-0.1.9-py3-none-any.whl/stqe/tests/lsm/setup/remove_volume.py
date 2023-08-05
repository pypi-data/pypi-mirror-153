#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.lsm import yield_lsm_config
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, clean_var
from os import environ


def remove_volume():
    print("INFO: Removing volume.")
    errors = []

    var_name = "LSM_" + environ["fmf_vol_id"]
    vol_id = read_var(var_name)

    config = list(yield_lsm_config())[0]
    if 'smis' in config['protocol']:
        print("smis protocol does not support ag removal on EMC. skipping.")
        return errors
    lsm = LibStorageMgmt(disable_check=True, **config)

    atomic_run("Removing volume %s" % vol_id,
               command=lsm.volume_delete,
               vol=vol_id,
               force=True,
               errors=errors)

    atomic_run("Removing var %s" % var_name,
               command=clean_var,
               var=var_name,
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = remove_volume()
    exit(parse_ret(errs))
