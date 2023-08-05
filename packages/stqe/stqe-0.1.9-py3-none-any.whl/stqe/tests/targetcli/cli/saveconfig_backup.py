#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.lio import TargetCLI
from libsan.host.cmdline import run
from time import sleep
import os


def count_files(directory):
    if not os.path.isdir(directory):
        return None
    number = len(os.listdir(directory))
    return number


def saveconfig_test_compare():
    errors = []
    target = TargetCLI()
    max_files = 0

    ret, data = atomic_run("Getting parameter max_backup_files from group global",
                           return_output=True,
                           command=target.get,
                           group="global",
                           max_backup_files="max_backup_files",
                           errors=errors
                           )
    if ret == 0:
        max_files = int(data.split("=")[1])

    ret = count_files("/etc/target/backup/")

    if not ret:
        print("FAIL: Backup directory does not exist.")
        errors.append("FAIL: Backup directory does not exist.")
    elif ret > max_files:
        print("FAIL: In backup directory is more files than max_backup_file!")
        errors.append("FAIL: In backup directory is more files than max_backup_file!")

    return errors


def saveconfig_create():
    errors = []
    target = TargetCLI()
    backups = int(os.environ["fmf_number_of_backups"])

    for i in range(backups):
        atomic_run("Creating saveconfig.json number %s" % i,
                   command=target.saveconfig,
                   errors=errors
                   )

    number = count_files("/etc/target/backup/")

    if number > 1:
        print("FAIL: In '/etc/target/backup/' is more than 1 backup file.")
        errors.append("FAIL: In '/etc/target/backup/' is more than 1 backup file.")
        return errors

    saveconfig_test_compare()

    return errors


def saveconfig_fail():
    errors = []
    target = TargetCLI()
    ret, data = atomic_run("Getting parameter max_backup_files from group global",
                           return_output=True,
                           command=target.get,
                           group="global",
                           max_backup_files="max_backup_files",
                           errors=errors
                           )

    maximum = int(data.split("=")[1])
    for i in range(maximum + 2):
        target.path = "/backstores/fileio"

        atomic_run("Creating fileio object number: %s." % i,
                   name="saveconfig%s" % i,
                   file_or_dev="/var/tmp/saveconfig_file%s" % i,
                   size="1",
                   command=target.create,
                   errors=errors
                   )

        target.path = ""

        atomic_run("Creating saveconfig.json number %s" % i,
                   command=target.saveconfig,
                   errors=errors
                   )
        sleep(1)

    ret = count_files("/etc/target/backup/")

    if not ret:
        print("FAIL: Backup directory does not exist.")
        errors.append("FAIL: Backup directory does not exist.")
    elif maximum != ret:
        print("FAIL: In backup directory is more files than max_backup_file!")
        errors.append("FAIL: In backup directory is more files than max_backup_file!")

    target.path = "/backstores/fileio"

    for i in range(maximum + 2):
        atomic_run("Removing fileio object number: %s" % i,
                   name="saveconfig%s" % i,
                   command=target.delete,
                   errors=errors
                   )

        atomic_run("Removing saveconfig file",
                   cmd="rm -f /var/tmp/saveconfig_file%s" % i,
                   command=run,
                   errors=errors
                   )
    return errors


def saveconfig_cleanup():
    errors = []

    atomic_run("Removing backups from /etc/target/backup",
               cmd="rm -rf /etc/target/backup/*",
               command=run,
               errors=errors
               )

    atomic_run("Removing saveconfig.json",
               cmd="rm -rf /etc/target/saveconfig.json",
               command=run,
               errors=errors
               )
    if errors:
        print("Cleanup failed")
        errors.append("Cleanup failed")

    return errors


if __name__ == "__main__":
    if int(os.environ['fmf_tier']) == 1:
        errs = saveconfig_create()
        errs += saveconfig_cleanup()
    if int(os.environ['fmf_tier']) == 2:
        errs = saveconfig_fail()
        errs += saveconfig_cleanup()
    exit(parse_ret(errs))
