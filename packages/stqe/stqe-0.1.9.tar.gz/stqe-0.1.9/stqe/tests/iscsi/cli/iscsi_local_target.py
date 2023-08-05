#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import libsan.host.fio as fio
import libsan.host.scsi as scsi
from stqe.host.persistent_vars import read_var
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.iscsi import discovery_st, node_login, clean_up


def do_io(device):  # fio - running randwrite until the 1G device is full, than verifying written data using CRC32C.
    if not fio.install_fio():
        print('FAIL: Unable to install fio')
        return False

    fio_params = {'bs': '4k', 'direct': 1, 'ioengine': 'libaio', 'iodepth': 16, 'verify': 'crc32c', 'verify_fatal': 1,
                  'do_verify': 1, 'rw': 'randwrite', 'runtime': 120}  # adding runtime cap of 2 minutes

    if not fio.fio_stress(device, verbose=True, **fio_params):
        print('FIO I/O failed')
        return False

    return True


def iscsi_local():
    errors = []
    ip_address = "127.0.0.1"
    target_iqn = read_var("TARGET_IQN")

    atomic_run("Discovering local target",
               target=ip_address,
               disc_db=True,
               command=discovery_st,
               errors=errors
               )

    atomic_run("Trying to login to portal: %s" % ip_address,
               target=target_iqn,
               command=node_login,
               errors=errors
               )

    ret = atomic_run("Getting free scsi disks",
                     filter_only={'vendor': 'LIO-ORG'},
                     command=scsi.get_free_disks,
                     errors=errors
                     )

    try:
        test_dev = '/dev/' + list(ret.keys())[0]
    except IndexError:
        msg = "FAIL: Could not find any free SCSI disk!"
        print(msg)
        errors.append(msg)
        return errors

    atomic_run("Running fio stress on device %s" % test_dev,
               device=test_dev,
               command=do_io,
               errors=errors
               )

    atomic_run("Cleaning up",
               command=clean_up,
               errors=errors
               )

    return errors


if __name__ == "__main__":
    errs = iscsi_local()
    exit(parse_ret(errs))
