#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.lsm import yield_lsm_config
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var


def unmask_volume():
    print("INFO: Unmasking volume.")
    errors = []

    vol_id = read_var("LSM_VOL_ID")
    ag_id = read_var("LSM_AG_ID")

    lsm = LibStorageMgmt(disable_check=True, **list(yield_lsm_config())[0])

    atomic_run("Unmasking volume %s to access group %s" % (vol_id, ag_id),
               command=lsm.volume_unmask,
               vol=vol_id,
               ag=ag_id,
               errors=errors)
    return errors


if __name__ == "__main__":
    errs = unmask_volume()
    exit(parse_ret(errs))
