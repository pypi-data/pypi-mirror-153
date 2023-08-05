#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import libsan.host.linux as linux
import libsan.host.targetd as targetd
from time import sleep
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret


def targetd_ssl_func_test():
    errors = []

    arguments = dict()

    arguments["password"] = os.environ["fmf_ssl_password"]
    arguments["key"] = os.environ["fmf_key"]

    atomic_run("Starting targetd SSL NO CERT test",
               enable=True,
               command=targetd.ssl_change,
               errors=errors
               )

    atomic_run("Adding password to the config",
               password=arguments["password"],
               command=targetd.set_password,
               errors=errors
               )

    atomic_run("Creating SSL key",
               name=arguments["key"],
               command=targetd.gen_ssl_key,
               errors=errors
               )

    atomic_run("Trying to start targetd without SSL cert, it should fail!",
               service_name="targetd",
               command=linux.service_restart,
               errors=errors
               )

    print("Waiting 10 seconds for the service to restart")
    sleep(10)

    atomic_run("Getting service status",
               retcode=3,
               command=targetd.targetd_status,
               errors=errors
               )

    atomic_run("Removing password from config",
               command=targetd.set_password,
               errors=errors
               )

    atomic_run("Removing SSL key: %s" % arguments["key"],
               name=arguments["key"] + ".pem",
               command=targetd.remove_file,
               errors=errors
               )

    cmd = "systemctl status targetd -l"
    has_systemctl = True

    if run("which systemctl", verbose=False) != 0:
        has_systemctl = False
    if not has_systemctl:
        cmd = "service targetd status -l"

    ret, data = run(cmd, return_output=True)
    for line in data.splitlines():
        if "ERROR:root:SSL file: '/etc/target/targetd_cert.pem' does not exist" in line:
            return errors

    print("FAIL: Service has failed with different error than expected or service is running!")
    errors.append("FAIL: Service has failed with different error than expected or service is running!")

    return errors


if __name__ == "__main__":
    errs = targetd_ssl_func_test()
    exit(parse_ret(errs))
