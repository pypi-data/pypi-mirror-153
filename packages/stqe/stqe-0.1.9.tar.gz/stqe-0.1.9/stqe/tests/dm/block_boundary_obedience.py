#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_env, read_var
from libsan.host.lvm import vg_create, lv_create, vg_remove, pv_remove
from libsan.host.linux import mkdir, rmdir, mkfs, mount, umount, get_system_logs
import time

start = time.mktime(time.localtime())

error = list()

device = read_var("LOOP1")
if not device:
    error.append("FAIL: Could not get the device from read_var")
    exit(parse_ret(error))
atomic_run("the device is loop1",
           command=run,
           cmd="lsblk | grep %s" % device.split('/')[2],
           return_output=True,
           errors=error)

# SETUP
parted = ["parted -s %s mklabel MSDOS" % device,
          "parted -s %s mkpart pri 1 1248" % device,
          "parted -s %s mkpart ext 1249 3814" % device,
          "parted -s %s mkpart log 1249 1728" % device,
          "parted -s %s mkpart log 1729 1760" % device,
          "parted -s %s mkpart log 1761 2016" % device,
          "parted -s %s mkpart log 2017 2047" % device,
          "parted -s %s mkpart log 2048 2687" % device,
          "parted -s %s mkpart log 2688 3007" % device,
          "parted -s %s mkpart log 3008 3320" % device,
          "parted -s %s mkpart log 3321 3336" % device,
          "parted -s %s mkpart log 3337 3814" % device]
for cmd in parted:
    atomic_run("Running parted cmd '%s'" % cmd,
               command=run,
               cmd=cmd,
               errors=error)
atomic_run("Running udevadm trigger",
            command=run,
            cmd="udevadm trigger",
            errors=error)
atomic_run("Running lsblk cmd",
            command=run,
            cmd="lsblk | grep loop",
            errors=error)
atomic_run("Creating VG 'vgtest'",
           command=vg_create,
           vg_name="vgtest",
           pv_name="%s" % device + (" %s" % device).join(["p" + str(x) for x in [1, 5, 8, 9, 10, 11, 13]]),
           errors=error)
atomic_run("Creating LV",
           command=lv_create,
           lv_name="testvol",
           vg_name="vgtest",
           options=["-l 100%FREE", "-y"],
           errors=error)
atomic_run("Creating filesystem",
           command=mkfs,
           device_name="/dev/mapper/vgtest-testvol",
           fs_type="xfs",
           errors=error)
atomic_run("Creating mount dir",
           command=mkdir,
           new_dir="/tmp/test_mount",
           errors=error)
atomic_run("Mounting to /tmp/test_mount",
           command=mount,
           device="/dev/mapper/vgtest-testvol",
           mountpoint="/tmp/test_mount",
           errors=error)
# TEST

atomic_run("Creating test file",
           command=run,
           cmd="dd if=/dev/urandom of=/tmp/test_mount/test_file bs=3K count=1128966 status=progress",
           expected_ret=1,
           expected_out="No space left on device",
           errors=error)
atomic_run("Syncing mount point",
           command=run,
           cmd="sync /tmp/test_mount",
           errors=error)
atomic_run("Removing test file",
           command=run,
           cmd="rm -f /tmp/test_mount/test_file",
           errors=error)
atomic_run("Syncing mount point",
           command=run,
           cmd="sync /tmp/test_mount",
           errors=error)
atomic_run("Sending trim",
           command=run,
           cmd="fstrim /tmp/test_mount",
           expected_out=read_env("fmf_expected_fstrim_out"),
           expected_ret=read_env("fmf_expected_fstrim_ret"),
           errors=error)

ret, syslogs = atomic_run(message="Checking logs for errors.",
                          command=get_system_logs,
                          since="-%s" % int(time.mktime(time.localtime()) - start),
                          return_output=True,
                          errors=error)
sys_error = "attempt to access beyond end of device"
if sys_error in syslogs:
    error.append("FAIL: Found error '%s' in syslog." % sys_error)

# CLEANUP
atomic_run("Umounting/tmp/test_mount",
           command=umount,
           mountpoint="/tmp/test_mount",
           errors=error)
atomic_run("Removing mount dir",
           command=rmdir,
           dir_name="/tmp/test_mount",
           errors=error)
atomic_run("Removing VG 'vgtest'",
           command=vg_remove,
           vg_name="vgtest",
           force=True,
           errors=error)
for pv in [" %sp" % device + str(x) for x in [1, 5, 8, 9, 10, 11, 13]]:
    atomic_run("Removing PV %s" % pv,
               command=pv_remove,
               pv_name=pv,
               errors=error)
atomic_run("Removing partitioning table",
           command=run,
           cmd="dd if=/dev/zero of=%s bs=512 count=1" % device,
           errors=error)
atomic_run("Reloading partitioning table",
           command=run,
           cmd="partprobe %s" % device,
           errors=error)

exit(parse_ret(error))
