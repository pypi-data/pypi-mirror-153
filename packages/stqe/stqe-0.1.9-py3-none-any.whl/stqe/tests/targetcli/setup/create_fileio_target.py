#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.persistent_vars import write_var, read_var
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.lio import TargetCLI
from os import environ


def remove_nones(kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


def create_iscsi():
    errors = []
    target_iqn = None
    tpg = None
    args = dict(storage_object=None, lun=None)
    args["storage_object"] = "/backstores/fileio/" + read_var("FILEIO_NAME")
    try:
        args["lun"] = environ["fmf_lun_id"]
    except KeyError:
        pass
    target = TargetCLI(path="/iscsi")

    ret, data = atomic_run("Creating iscsi",
                           return_output=True,
                           command=target.create,
                           errors=errors
                           )

    if ret != 0:
        print("FAIL: Could not create iscsi target !")
        errors.append("FAIL: Could not create iscsi target !")
        return errors

    lines = data.splitlines()
    for line in lines:
        if "iqn" in line:
            target_iqn = line.split()[2][:-1]
            continue
        if "TPG" in line:
            tpg = "tpg" + line.split()[2][:-1]
            continue

    target.path = "/iscsi/" + target_iqn + "/" + tpg + "/" + "luns"

    atomic_run("Creating lun with storage object: %s" % args["storage_object"],
               command=target.create,
               errors=errors,
               **remove_nones(args)
               )

    target.path = "/iscsi/" + target_iqn + "/" + tpg

    atomic_run("Setting parameter generate_node_acls to '1'",
               generate_node_acls=1,
               group="attribute",
               command=target.set,
               errors=errors
               )

    atomic_run("Setting parameter demo_mode_write_protect to '0'",
               demo_mode_write_protect=0,
               group="attribute",
               command=target.set,
               errors=errors
               )

    atomic_run("Writing var TPG",
               command=write_var,
               var={"TPG": tpg},
               errors=errors)

    atomic_run("Writing var TARGET IQN",
               command=write_var,
               var={"TARGET_IQN": target_iqn},
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = create_iscsi()
    exit(parse_ret(errs))
