#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import write_var
from libsan.host.linux import os_arch
from os import environ


def _is_wwpn(init):
    if len(init.split(":")) == 8:
        return True
    return False


def configure_lsm(protocols, username=None, password=None, target=None, **kwargs):
    print("INFO: Setting up libstoragemgmt for protocol %s." % protocols[0])
    arguments = locals()
    if 'kwargs' in arguments:
        kwargs = arguments.pop('kwargs')
        for kwarg in kwargs:
            arguments[kwarg] = kwargs[kwarg]

    errors = []

    for argument in arguments.keys():
        if arguments[argument] is None:
            continue

        var = "LSM_" + argument.upper()
        value = arguments[argument]
        # to write [val1, val2] instead of ['val1', 'val2']
        if isinstance(value, list):
            value = "[%s]" % ", ".join(value[:])
        atomic_run("Writing var %s" % var,
                   command=write_var,
                   var={'%s' % var: value},
                   errors=errors)

    return errors


if __name__ == "__main__":
    # list of variables to save in /tmp as persistent vars
    arguments = {
        'protocols': [],
        'username': None,
        'password': None,
        'target': None,
        'timeout': None,
        'pool_id': None,
        'pool_id_volume': None,
        'fs_size': None,
        'fs_export_path': None,
        'rw_host': None,
        'sys_id': None,
        'vol_size': None,
        'vol_size_2': None,
        'system_read_pct': None,
        'chap_in_pass': None,
        'chap_out_pass': None
    }
    for argument in arguments.keys():
        try:
            arguments[argument] = environ['fmf_' + argument]
        except KeyError:
            pass

    # these need to be arch specific
    arch = os_arch().replace("_", "-") # '_' is invalid in IQN
    arguments_arch = {
        'fs_name': None,
        'pool_name': None,
        'fs_cloned_name': None,
        'fs_snap_name': None,
        'ag_name': None,
        'ag_name_2': None,
        'init_id': None,
        'init_id_chap': None,
        'init_id_2': None,
        'vol_name': None,
        'vol_name_2': None,
        'vol_rep_name': None,
        'chap_in_user': None,
        'chap_out_user': None
    }
    for argument in arguments_arch.keys():
        try:
            arguments_arch[argument] = environ['fmf_' + argument]
            if 'init' in argument and _is_wwpn(arguments_arch[argument]):
                continue
            arguments_arch[argument] += "-%s" % arch
            # FS name cannot contain '-', INVALID_ARGUMENT(101)
            if any(x in argument for x in ['fs_name', 'fs_cloned_name', 'fs_snap_name']):
                arguments_arch[argument] = arguments_arch[argument].replace("-", "_")
        except KeyError:
            pass
    arguments.update(arguments_arch)

    try:
        if not arguments['protocols'].startswith("["):
            raise AttributeError
        arguments['protocols'] = arguments['protocols'][1:-1].split(", ")
    except AttributeError:
        print("ERROR: Protocols must be type list.")
        exit(1)

    errs = configure_lsm(**arguments)
    exit(parse_ret(errs))