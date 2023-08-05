#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret
from os import environ
from libsan.host.linux import dist_release


def signatures(modules):
    # Check signatures of given modules.
    errors = []
    arguments = []

    if float(dist_release()) > 7.0:
        print("WARN: On modules are not signed yet on RHEL 8!")
        # later use keyring %:.builtin_trusted_keys when they get signed
        return errors

    if not isinstance(modules, list):
        return ["Signatures test requires modules parameter as list type, got %s" % type(modules)]

    for module in modules:
        cmd = "keyctl list %:.system_keyring | grep $(modinfo " + str(module) + " | grep sig_key " + \
              "| awk '{print tolower($2)}' | sed 's/\://g')"
        arguments += [
            # signature checking
            {'message': "Finding sig_key of module '%s'." % module, 'command': run,
             'cmd': 'modinfo %s | grep sig_key' % module},
            {'message': "Getting more info on module '%s' signature." % module, 'command': run,
             'cmd': cmd}
        ]

    for argument in arguments:
        atomic_run(errors=errors,
                   **argument)

    return errors


if __name__ == "__main__":
    if int(environ['fmf_tier']) == 1:
        errs = signatures(["uds", "kvdo"])
    exit(parse_ret(errs))
