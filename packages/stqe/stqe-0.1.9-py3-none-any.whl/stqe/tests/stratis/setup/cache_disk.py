#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.stratis import Stratis
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, read_env, write_var
import time


def create_cache_disk():
    errors = []
    stratis = Stratis()
    pool_name = read_env('fmf_pool_name')

    id = ""
    try:
        id = "_" + str(read_env("fmf_id"))
        pool_name = pool_name + id
    except KeyError:
        pass

    previous = ""
    try:
        previous = int(id[1:]) - 1
        if previous == 1:
            previous = ""
        else:
            previous = "_" + str(previous)
    except ValueError:
        pass
    print("previous is %s, id is %s," % (previous, id))
    blockdevs = read_var("STRATIS_FREE%s" % previous)
    # if blockdevs is None:
    #    blockdevs = read_var("STRATIS_DEVICE")

    if "init_cache" in read_env("fmf_name"):
        if not isinstance(blockdevs, list):
            blockdevs = [blockdevs]
        free = blockdevs[:]
        if free:
            cache_disk = free.pop()
            # atomic_run("Writing var CACHE_DISK%s" % id,
            #       command=write_var,
            #       var={'CACHE_DISK%s' % id: cache_disk},
            #       errors=errors)
            atomic_run("Writing var STRATIS_FREE%s" % id,
                       command=write_var,
                       var={'STRATIS_FREE%s' % id: free},
                       errors=errors)

    time.sleep(2)
    atomic_run(message="Triggering udev",
               command=run,
               cmd="udevadm trigger; udevadm settle",
               errors=errors)

    atomic_run("statis pool init cache %s." % pool_name,
               command=stratis.pool_init_cache,
               pool_name=pool_name,
               blockdevs=cache_disk,
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = create_cache_disk()
    exit(parse_ret(errs))
