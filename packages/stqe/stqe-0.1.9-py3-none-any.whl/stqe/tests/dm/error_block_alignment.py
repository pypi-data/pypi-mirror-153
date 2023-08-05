#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_env

# SETUP
run("dmsetup create tst_zero --table '0 131072 zero'")
run("dmsetup create tst_error --table '0 131072 error';")
run("""dmsetup create tst_err_writes << EOF
 0 22480 linear /dev/mapper/tst_zero 0
 22480 32 delay /dev/mapper/tst_zero 22480 0 /dev/mapper/tst_error 22480 0
 22512 108560 linear /dev/mapper/tst_zero 22512
EOF""")
# TEST

error = list()
try:
    expected_out = read_env("fmf_expected_out")
except KeyError:
    expected_out = "+0 records in"

try:
    expected_ret = read_env("fmf_expected_ret")
except KeyError:
    expected_ret = 0

atomic_run(message="Testing aligned",
           command=run,
           cmd="dd if=/dev/mapper/tst_err_writes of=/dev/mapper/tst_err_writes bs=4M iflag=direct oflag=direct;",
           expected_ret=expected_ret, expected_out=expected_out, errors=error)

atomic_run(message="Testing misaligned.",
           command=run,
           cmd="dd if=/dev/mapper/tst_err_writes of=/dev/mapper/tst_err_writes bs=2M iflag=direct oflag=direct",
           expected_ret=expected_ret, expected_out=expected_out, errors=error)
# CLEANUP
run("dmsetup remove tst_err_writes;")
run("dmsetup remove tst_error")
run("dmsetup remove tst_zero")

exit(parse_ret(error))
