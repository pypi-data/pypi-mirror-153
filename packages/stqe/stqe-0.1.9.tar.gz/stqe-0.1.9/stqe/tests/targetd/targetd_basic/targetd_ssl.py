#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import libsan.host.linux as linux
import libsan.host.targetd as targetd
from time import sleep
from stqe.host.atomic_run import atomic_run, parse_ret


def targetd_ssl_test():
    errors = []

    arguments = dict()

    arguments["password"] = os.environ["fmf_ssl_password"]
    arguments["key"] = os.environ["fmf_key"]
    arguments["cert"] = os.environ["fmf_cert"]

    atomic_run("Starting targetd SSL test",
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

    atomic_run("Creating SSL certificate",
               name=arguments["cert"],
               key_name=arguments["key"],
               command=targetd.gen_ssl_cert,
               errors=errors
               )

    atomic_run("Targetd configured properly.... starting targetd service",
               service_name="targetd",
               command=linux.service_restart,
               errors=errors
               )

    print("Waiting 10 seconds for the service to restart")
    sleep(10)

    atomic_run("Getting service status",
               command=targetd.targetd_status,
               errors=errors
               )

    atomic_run("Checking TLS status",
               command=targetd.tls_status,
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

    atomic_run("Removing SSL cert: %s" % arguments["cert"],
               name=arguments["cert"] + ".pem",
               command=targetd.remove_file,
               errors=errors
               )

    atomic_run("Removing SSL key: %s" % arguments["key"],
               name=arguments["key"] + ".pem",
               command=targetd.remove_file,
               errors=errors
               )

    return errors


if __name__ == "__main__":
    errs = targetd_ssl_test()
    exit(parse_ret(errs))
