#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config
from os import environ
from stqe.host.persistent_vars import read_var


def iscsi_chap_success():
    errors = []

    init = read_var("LSM_INIT_ID_CHAP")
    in_user = read_var("LSM_CHAP_IN_USER")
    in_pass = read_var("LSM_CHAP_IN_PASS")
    out_user = read_var("LSM_CHAP_OUT_USER")
    out_pass = read_var("LSM_CHAP_OUT_PASS")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        atomic_run("Setting up CHAP auth without credentials with protocol %s" % config['protocol'],
                   command=lsm.iscsi_chap,
                   init=init,
                   errors=errors)

        atomic_run("Setting up CHAP auth with IN credentials with protocol %s" % config['protocol'],
                   command=lsm.iscsi_chap,
                   init=init,
                   in_user=in_user,
                   in_pass=in_pass,
                   errors=errors)

        atomic_run("Setting up CHAP auth with OUT credentials with protocol %s" % config['protocol'],
                   command=lsm.iscsi_chap,
                   init=init,
                   out_user=out_user,
                   out_pass=out_pass,
                   errors=errors)

        atomic_run("Setting up CHAP auth with all credentials with protocol %s" % config['protocol'],
                   command=lsm.iscsi_chap,
                   init=init,
                   in_user=in_user,
                   in_pass=in_pass,
                   out_user=out_user,
                   out_pass=out_pass,
                   errors=errors)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = iscsi_chap_success()
    exit(parse_ret(errs))
