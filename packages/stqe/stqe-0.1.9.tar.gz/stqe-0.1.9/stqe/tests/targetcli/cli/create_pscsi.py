#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import os
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var
from libsan.host.lio import TargetCLI


def create_pscsi():
    errors = []

    target = TargetCLI(path="/backstores/pscsi")

    scsi_id = read_var("SCSI_ID")
    name = os.environ["fmf_pscsi_name"]

    atomic_run("Creating backstore pscsi object with name: %s" % name,
               name=name,
               dev=scsi_id,
               command=target.create,
               errors=errors
               )

    atomic_run("Deleting pscsi object %s" % name,
               name=name,
               command=target.delete,
               errors=errors
               )

    return errors


if __name__ == "__main__":
    errs = create_pscsi()
    exit(parse_ret(errs))
