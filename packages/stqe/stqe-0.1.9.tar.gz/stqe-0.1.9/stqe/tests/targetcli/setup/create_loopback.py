#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, write_var
from libsan.host.scsi import get_scsi_disk_ids
from libsan.host.lio import TargetCLI
from libsan.host.linux import wait_udev
from os import environ


def create_tpg_lun():
    errors = []
    disk_id = None

    target = TargetCLI(path="/loopback")

    lun = environ["fmf_lun"]
    storage_object = read_var("FILEIO_NAME")

    ret, data = atomic_run("Creating loopback",
                           return_output=True,
                           command=target.create,
                           errors=errors
                           )

    wwn = data.split()[2][:-1]

    target.path = "/loopback/" + wwn + "/luns"

    atomic_run("Creating lun with name: %s" % lun,
               command=target.create,
               storage_object="/backstores/fileio/" + storage_object,
               lun=lun,
               errors=errors
               )

    atomic_run("Waiting udev to finish storage scan",
               command=wait_udev,
               errors=errors
               )

    scsi_ids = get_scsi_disk_ids()

    for scsi_id in scsi_ids:
        if lun == scsi_id.split(":")[3]:
            disk_id = scsi_id

    atomic_run("Writing var SCSI_ID",
               command=write_var,
               var={"SCSI_ID": disk_id},
               errors=errors)

    atomic_run("Writing var LOOPBACK_WWN",
               command=write_var,
               var={"LOOPBACK_WWN": wwn},
               errors=errors)

    atomic_run("Writing var LOOPBACK_LUN",
               command=write_var,
               var={"LOOPBACK_LUN": lun},
               errors=errors
               )

    return errors


if __name__ == "__main__":
    errs = create_tpg_lun()
    exit(parse_ret(errs))
