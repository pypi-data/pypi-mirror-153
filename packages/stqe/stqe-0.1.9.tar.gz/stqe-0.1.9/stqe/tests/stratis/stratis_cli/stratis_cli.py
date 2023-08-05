#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.stratis import Stratis
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_env
from stqe.host.fmf_tools import get_env_args, get_func_from_string
from stqe.host.stratis import get_stratis_args


def call_func(args, stratis_object, errors):
    name = read_env("fmf_name")
    if "init_cache/success" in name or "add_cache/success" in name or "add_data/success" in name:
        if "single" in name:
            # Need to take only 1 device
            args['blockdevs'] = args['blockdevs'].pop()
        if "add_cache/success/multiple" in name or "init_cache/success/multiple" in name:
            # using all would trigger error, cache is limited to 32TB
            args['blockdevs'] = args['blockdevs'][:2]
    if "fail/device_instead_of_pool_name" in name or "blockdev/list/fail/device_instead_of_name" in name or \
            "fs/list/fail/device_instead_of_name" in name:
        args['pool_name'] = args['pool_name'].pop()
    if "snapshot/fail/device_instead_of_snapshot_name" in name:
        args['origin_name'] = args['origin_name'].pop()
    if "pool/create/fail/no_pool_name" in name:
        args['blockdevs'] = args['blockdevs'].pop()

    return args


def stratis_cli():
    errors = []
    stratis = Stratis()
    args = get_stratis_args(stratis_object=stratis)
    # some extra args for some setups
    args.update(get_env_args({}))
    args = call_func(args, stratis, errors)
    if args is None:
        return errors

    print("stqe/stratis_cli args is %s" % args)
    command_string = args['command']
    args['command'] = get_func_from_string(stratis, args.pop('command'), local_functions=globals())

    ret = atomic_run(errors=errors,
                     **args)

    check_clean(ret=ret, stratis_object=stratis, args=args, errors=errors, command=command_string)

    return errors


def check_clean(**kwargs):
    if "pool/rename/success" in read_env("fmf_name"):
        _, data = atomic_run("Listing stratis pools.",
                             command=kwargs['stratis_object'].pool_list,
                             return_output=True,
                             errors=kwargs['errors'])
        if kwargs['args']['new'] not in data:
            msg = "FAIL: Did not rename stratis pool %s to %s." % (kwargs['args']['current'], kwargs['args']['new'])
            print(msg)
            kwargs['errors'].append(msg)

    if "fs/rename/success" in read_env("fmf_name"):
        _, data = atomic_run("Listing stratis fs on pool.",
                             command=kwargs['stratis_object'].fs_list,
                             pool_name=kwargs["args"]["pool_name"],
                             return_output=True,
                             errors=kwargs['errors'])
        if kwargs['args']['new_name'] not in data:
            msg = "FAIL: Did not rename stratis pool %s to %s." % (
                kwargs['args']['fs_name'], kwargs['args']['new_name'])
            print(msg)
            kwargs['errors'].append(msg)

    if "key/" in read_env("fmf_name"):
        _, data = atomic_run("Listing stratis pools.",
                             command=kwargs['stratis_object'].pool_list,
                             return_output=True,
                             errors=kwargs['errors'])
        _, data = atomic_run("Listing blockdev .",
                             command=kwargs['stratis_object'].blockdev_list,
                             return_output=True,
                             errors=kwargs['errors'])

        _, data = atomic_run("Listing blockdev .",
                             command=kwargs['stratis_object'].key_list,
                             return_output=True,
                             errors=kwargs['errors'])

    return


if __name__ == "__main__":
    errs = stratis_cli()
    exit(parse_ret(errs))
