#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config, get_local_disk_data
from os import environ


def local_disk_fault_led_success():
    errors = []

    lsm = LibStorageMgmt(disable_check=True, **list(yield_lsm_config())[0])
    ret, disks = atomic_run("Listing local disks",
                            command=lsm.local_disk_list,
                            return_output=True,
                            script=True,
                            errors=errors)
    data = get_local_disk_data(disks)
    if not data:
        print("WARN: Could not find any local disks, skipping.")
        return errors

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        for disk in data:
            if data[disk]["LED Status"] == "Unknown":
                print("WARN: Disk %s does not support LED changes." % disk)
                continue
            status = data[disk]["LED Status"]
            arguments = [
                {'message': "Switching fault LED ON with protocol %s" % config['protocol'],
                 'command': lsm.local_disk_ident_led_on},
                {'message': "Switching fault LED OFF with protocol %s" % config['protocol'],
                 'command': lsm.local_disk_ident_led_off}
            ]
            if status == "ON":
                arguments = reversed(arguments)
            for argument in arguments:
                atomic_run(path=disk,
                           errors=errors,
                           **argument)
    return errors


def local_disk_fault_led_on_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail to set fault led ON without path with protocol %s" % config['protocol'],
             'command': lsm.local_disk_fault_led_on},
            {'message': "Trying to fail to set fault led ON with wrong path with protocol %s" % config['protocol'],
             'command': lsm.local_disk_fault_led_on, 'path': "WRONG"}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def local_disk_fault_led_off_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail to set fault led OFF without path with protocol %s" % config['protocol'],
             'command': lsm.local_disk_fault_led_off},
            {'message': "Trying to fail to set fault led OFF with wrong path with protocol %s" % config['protocol'],
             'command': lsm.local_disk_fault_led_off, 'path': "WRONG"}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = local_disk_fault_led_success()
    if int(environ['fmf_tier']) == 2:
        errs = local_disk_fault_led_on_fail()
        errs += local_disk_fault_led_off_fail()
    exit(parse_ret(errs))
