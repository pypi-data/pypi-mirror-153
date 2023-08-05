#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.lio import TargetCLI
from libsan.host.cmdline import run
from hashlib import sha1
from json import load


def saveconfig_cleanup():
    errors = []

    atomic_run("Removing backups from /etc/target/backup",
               cmd="rm -f /etc/target/backup/*",
               command=run,
               errors=errors
               )

    atomic_run("Removing saveconfig.json",
               cmd="rm -f /etc/target/saveconfig.json",
               command=run,
               errors=errors
               )

    return errors


def compare_backup():
    errors = []
    target = TargetCLI()

    for i in range(2):
        atomic_run("Saving configuration...",
                   command=target.saveconfig,
                   errors=errors
                   )

    with open("/etc/target/saveconfig.json", "r") as last_save:
        saveconfig = load(last_save)
        hash_saveconfig = sha1(repr(saveconfig).encode('utf-8')).hexdigest()

    ret, data = atomic_run("Listing /etc/target/backup/ directory",
                           return_output=True,
                           cmd="ls -lt /etc/target/backup/",
                           command=run,
                           errors=errors
                           )

    lines = data.split()
    backup_file = "Does_not_exist"
    for line in lines:
        if "saveconfig" in line:
            backup_file = line
            break
    with open("/etc/target/backup/" + backup_file, "r") as backup:
        backup_config = load(backup)
        hash_backup = sha1(repr(backup_config).encode('utf-8')).hexdigest()

    if not hash_saveconfig == hash_backup:
        print("FAIL: Backup file is different than last saved configuration")
        errors.append("FAIL: Backup file is different than last saved configuration")

    return errors


if __name__ == "__main__":
    errs = compare_backup()
    errs += saveconfig_cleanup()
    exit(parse_ret(errs))
