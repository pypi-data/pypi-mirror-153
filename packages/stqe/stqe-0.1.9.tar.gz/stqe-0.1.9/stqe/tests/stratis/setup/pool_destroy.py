#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.stratis import Stratis
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, clean_var, read_env, write_var


def destroy_pool():
    errors = []
    stratis = Stratis()

    id = ""
    try:
        id = "_" + str(read_env("fmf_id"))
    except KeyError:
        pass
    pool_name = read_var("STRATIS_POOL%s" % id)

    if "single" in read_env("fmf_name"):
        free = read_var("STRATIS_FREE%s" % id)
        if not isinstance(free, list):
            free = [free]
        device = read_var("STRATIS_DEVICE%s" % id)
        if not isinstance(device, list):
            device = [device]
        write_var({"STRATIS_DEVICE%s" % id: free + device})
        clean_var("STRATIS_FREE%s" % id)

    atomic_run("Destroying statis pool %s." % pool_name,
               command=stratis.pool_destroy,
               pool_name=pool_name,
               errors=errors)

    atomic_run("Cleaning var STRATIS_POOL%s" % id,
               command=clean_var,
               var='STRATIS_POOL%s' % id,
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = destroy_pool()
    exit(parse_ret(errs))
