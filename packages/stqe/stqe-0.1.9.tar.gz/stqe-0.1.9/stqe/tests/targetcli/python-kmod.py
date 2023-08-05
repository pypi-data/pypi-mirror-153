#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.lio import TargetCLI
from libsan.host.linux import is_module_loaded


def test_python_kmod():
    errors = []
    targetcli = TargetCLI()

    atomic_run("INFO: Running targetcli get command.",
               group="global",
               command=targetcli.get,
               errors=errors
               )

    atomic_run("INFO: Checking if module is loaded",
               module_name="target_core_mod",
               command=is_module_loaded,
               errors=errors
               )

    return errors


if __name__ == "__main__":
    errs = test_python_kmod()
    exit(parse_ret(errs))
