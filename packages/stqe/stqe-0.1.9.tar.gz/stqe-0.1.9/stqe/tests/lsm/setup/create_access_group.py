#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.lsm import yield_lsm_config
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, write_var
from os import environ


def create_access_group():
    print("INFO: Creating AG.")
    errors = []

    ag_name = read_var("LSM_AG_NAME") + environ['fmf_init'].upper()
    sys_id = read_var("LSM_SYS_ID")
    init_id = read_var("LSM_INIT_ID" + environ['fmf_init'].upper())

    config = list(yield_lsm_config())[0]
    if 'smis' in config['protocol']:
        print("smis protocol does not support ag creation on EMC. skipping.")
        return errors
    lsm = LibStorageMgmt(disable_check=True, **config)

    ret, data = atomic_run("Creating AG '%s'." % ag_name,
                           command=lsm.access_group_create,
                           name=ag_name,
                           init=init_id,
                           sys=sys_id,
                           return_output=True,
                           errors=errors)

    for line in data.splitlines():
        if ag_name in line:
            ag_id = line.split()[0].strip()
            atomic_run("Writing var LSM_AG_ID" + environ['fmf_init'].upper(),
                       command=write_var,
                       var={"LSM_AG_ID" + environ['fmf_init'].upper(): ag_id},
                       errors=errors)

    return errors


if __name__ == "__main__":
    errs = create_access_group()
    exit(parse_ret(errs))
