#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import os
from stqe.host.atomic_run import parse_ret
from libsan.host.cmdline import run
from libsan.host.linux import dist_ver, dist_name


def tcmu_runner_install():
    errors = []

    repo = os.environ["fmf_tcmu_repo_link"]  # "https://github.com/open-iscsi/tcmu-runner.git"
    path = os.environ["fmf_tcmu_path"]
    if os.path.isdir(path):
        print("Directory %s already exists! Skipping installation." % path)
        return errors

    packages = "cmake make gcc libnl3 glib2 zlib kmod libnl3-devel glib2-devel zlib-devel " \
               "kmod-devel librados2 librados2-devel librbd1 librbd1-devel qemu-img"

    cmd = "git clone %s %s" % (repo, path)
    ret = run(cmd)
    if ret != 0:
        msg = "FAIL: Could not clone repo %s to directory %s" % (repo, path)
        print(msg)
        errors.append(msg)
        return errors

    cmd = "dnf install -y %s " % packages
    if dist_name() != 'Fedora':
        cmd += "--enablerepo=rhel-buildroot"
        if float(dist_ver() < 8.0):
            cmd = "yum install -y %s" % packages

    ret = run(cmd)
    if ret != 0:
        msg = "FAIL: Could not install all packages!"
        print(msg)
        errors.append(msg)
        return errors

    current_directory = os.path.abspath(os.curdir)
    os.chdir(path)

    cmd = "cmake . -Dwith-glfs=false -DSUPPORT_SYSTEMD=ON -DCMAKE_INSTALL_PREFIX=/usr"
    ret = run(cmd)
    if ret != 0:
        msg = "FAIL:Command 'cmake' exited with retcode=%s" % ret
        print(msg)
        errors.append(msg)
        return errors

    os.chdir(current_directory)

    cmd = "make --directory=%s" % path
    ret = run(cmd)
    if ret != 0:
        msg = "FAIL:Command 'make install' exited with retcode=%s" % ret
        print(msg)
        errors.append(msg)
        return errors

    cmd = "make install --directory=%s" % path
    ret = run(cmd)
    if ret != 0:
        msg = "FAIL:Command 'make install' exited with retcode=%s" % ret
        print(msg)
        errors.append(msg)
        return errors

    return errors


if __name__ == "__main__":
    errs = tcmu_runner_install()
    exit(parse_ret(errs))
