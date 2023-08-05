#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.lsm import LibStorageMgmt
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.lsm import yield_lsm_config, get_local_disk_data
from os import environ
from stqe.host.persistent_vars import read_var


def volume_ident_led_success():
    errors = []

    vol = read_var("LSM_VOL_ID")

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        ret, disks = atomic_run("Listing local disks before changing ident LED.",
                                command=lsm.local_disk_list,
                                return_output=True,
                                script=True,
                                errors=errors)
        data_before = get_local_disk_data(disks)

        atomic_run("Enabling ident LED of volume %s." % vol,
                   command=lsm.volume_ident_led_on,
                   vol=vol,
                   errors=errors)

        atomic_run("Disabling ident LED of volume %s." % vol,
                   command=lsm.volume_ident_led_off,
                   vol=vol,
                   errors=errors)

        ret, disks = atomic_run("Listing local disks after changing ident LED.",
                                command=lsm.local_disk_list,
                                return_output=True,
                                script=True,
                                errors=errors)
        data_after = get_local_disk_data(disks)

        if data_before != data_after:
            atomic_run("Enabling ident LED to return it to previous state with protocol %s." % config['protocol'],
                       command=lsm.volume_ident_led_on,
                       vol=vol,
                       errors=errors)
            ret, disks = atomic_run("Listing local disks after returning ident LED state.",
                                    command=lsm.local_disk_list,
                                    return_output=True,
                                    script=True,
                                    errors=errors)
            data_after = get_local_disk_data(disks)
            if data_before != data_after:
                msg = "FAIL: Could not return ident LED to previous state with protocol %s" % config['protocol']
                print(msg)
                errors.append(msg)

    return errors


def volume_ident_led_on_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail enabling ident LED for volume without any paramethers with protocol %s" %
                        config['protocol'], 'command': lsm.volume_ident_led_on},
            {'message': "Trying to fail enabling ident LED for volume with WRONG volume with protocol %s" %
                        config['protocol'], 'vol': "WRONG", 'command': lsm.volume_ident_led_on}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def volume_ident_led_off_fail():
    errors = []

    for config in yield_lsm_config():
        lsm = LibStorageMgmt(disable_check=True, **config)

        arguments = [
            {'message': "Trying to fail disabling ident LED for volume without any paramethers with protocol %s" %
                        config['protocol'], 'command': lsm.volume_ident_led_off},
            {'message': "Trying to fail disabling ident LED for volume with WRONG volume with protocol %s" %
                        config['protocol'], 'vol': "WRONG", 'command': lsm.volume_ident_led_off}
        ]
        for argument in arguments:
            atomic_run(expected_ret=2,
                       errors=errors,
                       **argument)
    return errors


def volume_ident_led_offline():
    errors = []
    # TODO: Check changing ident LED when volume is disabled, create test
    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = volume_ident_led_success()
    if int(environ['fmf_tier']) == 2:
        errs = volume_ident_led_on_fail()
        errs += volume_ident_led_off_fail()
    exit(parse_ret(errs))
