#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.lsm import yield_lsm_config, get_data_from_script_output
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var
from time import sleep

def cleanup_storage():
    errors = []

    ag_name = read_var("LSM_AG_NAME")
    ag_name_2 = read_var("LSM_AG_NAME_2")
    # fs_name = read_var("LSM_FS_NAME")
    # fs_cloned_name = read_var("LSM_FS_CLONED_NAME")
    # fs_snap_name = read_var("LSM_FS_SNAP_NAME")
    # vol_name = read_var("LSM_VOL_NAME")
    # vol_name_2 = read_var("LSM_VOL_NAME_2")
    # vol_rep_name = read_var("LSM_VOL_REP_NAME")

    config = list(yield_lsm_config())[0]
    if not config['protocol']:
        print("This is just local disk test, no need to clean up storage.")
        return errors

    lsm = LibStorageMgmt(disable_check=True, **config)

    ret, data = atomic_run("Listing access groups",
                           command=lsm.list,
                           lsm_type="ACCESS_GROUPS",
                           return_output=True,
                           script=True,
                           errors=errors)
    ags = get_data_from_script_output(data)
    for ag in [ag_name_2, ag_name]:
        ag_id = None
        if ags is None:
            break
        for ags_id in ags:
            if ags[ags_id]['Name'] == ag:
                ag_id = ags_id
                break
        if ag_id is None:
            print("INFO: Could not find ag %s, continuing." % ag)
            continue
        atomic_run("Removing AG '%s'." % ag,
                   command=lsm.access_group_delete,
                   ag=ag_id,
                   force=True,
                   errors=errors)
    # give some time to print all data
    sleep(1)

    return errors


if __name__ == "__main__":
    errs = cleanup_storage()
    exit(parse_ret(errs))
