#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import write_var, read_env
from libsan.host.cmdline import run
from libsan.host.linux import service_start, is_service_running, service_stop, install_package, hostname


def setup_tang():
    errors = []

    cleanup = None
    tang_service_name = "tangd.socket"

    install_package("tang")
    install_package("curl")
    install_package('jose')
    install_package('jq')
    install_package("coreutils")

    try:
        cleanup = read_env("fmf_tang_cleanup")
    except KeyError:
        pass

    if not cleanup:
        atomic_run("Start tang server",
                   command=service_start,
                   service_name=tang_service_name,
                   errors=errors
                   )

        if is_service_running("firewalld"):
            atomic_run("Stopping firewalld service",
                       command=service_stop,
                       service_name="firewalld",
                       errors=errors
                       )

        ret, data = atomic_run("Getting Tang thumbprint of server",
                               return_output=True,
                               command=run,
                               cmd=f'curl -s {hostname()}/adv | jq -r .payload | base64 -d |'
                                   f' jose jwk use -i- -r -u verify -o- | jose jwk thp -i- ',
                               errors=errors
                               )

        atomic_run("Writing var TANG_THUMBPRINT",
                   command=write_var,
                   var={'TANG_THUMBPRINT': data},
                   errors=errors)

        atomic_run("Writing var TANG_URL",
                   command=write_var,
                   var={'TANG_URL': f"http://{hostname()}"},
                   errors=errors)

        return errors

    atomic_run("Stopping tangd.socket",
               service_name=tang_service_name,
               command=service_stop,
               errors=errors
               )

    return errors


if __name__ == "__main__":
    errs = setup_tang()
    exit(parse_ret(errs))
