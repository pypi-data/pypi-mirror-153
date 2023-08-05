#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import libsan.host.linux as linux
import libsan.host.targetd as targetd
from time import sleep
from stqe.host.atomic_run import atomic_run, parse_ret


def targetd_basic_test():
    errors = []
    arguments = dict()

    arguments["password"] = os.environ["fmf_password"]

    atomic_run("Disabling SSL",
               command=targetd.ssl_change,
               errors=errors
               )

    atomic_run("Adding password to targetd config",
               password=arguments["password"],
               command=targetd.set_password,
               errors=errors
               )

    atomic_run("Restarting targetd service",
               service_name="targetd",
               command=linux.service_restart,
               errors=errors
               )

    print("Waiting 10 seconds for the service to restart")
    sleep(10)

    atomic_run("Getting targetd service status",
               command=targetd.targetd_status,
               errors=errors
               )

    atomic_run("Stopping targetd service",
               service_name="targetd",
               command=linux.service_stop,
               errors=errors
               )

    atomic_run("Removing password from config",
               command=targetd.set_password,
               errors=errors
               )

    return errors


if __name__ == "__main__":
    errs = targetd_basic_test()
    exit(parse_ret(errs))
