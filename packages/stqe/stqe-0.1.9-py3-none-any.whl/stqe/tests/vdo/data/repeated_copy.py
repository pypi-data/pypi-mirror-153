#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.vdo import VDOStats
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var, read_env
from stqe.host.vdo import is_block_device
from libsan.host.cmdline import run
from shutil import copy
from libsan.host.linux import compare_version
import libsan.misc.time as time


def single_copy(vdostats, device, vdo_name, fs_dir, file, duration):
    error = []
    file_name = "vdo_test.file"
    expected_ret = 0
    if compare_version("vdo", "6.2.0.0", "0") and not compare_version("vdo", "6.2.0.71", "71-4"):
        # Hit vdostats bug
        expected_ret = 1

    arguments = [
        {'message': "Copying file %s to %s/%s" % (file, fs_dir, file_name), 'command': copy, 'src': "%s" % file,
         'dst': "%s/%s" % (fs_dir, file_name)},
        {'message': "Umounting filesystem", 'command': run, 'cmd': "umount %s" % fs_dir},
        {'message': "Mounting XFS filesystem with discard enabled", 'command': run,
         'cmd': "mount -o discard %s %s" % (device, fs_dir)},
        {'message': "Removing file %s/%s" % (fs_dir, file_name), 'command': run,
         'cmd': "rm -f %s/%s" % (fs_dir, file_name)},
        {'message': "Umounting filesystem", 'command': run, 'cmd': "umount %s" % fs_dir},
        {'message': "Checking stats of vdo %s" % vdo_name, 'command': vdostats.stats, 'expected_ret': expected_ret},
        {'message': "Mounting XFS filesystem with discard enabled", 'command': run,
         'cmd': "mount -o discard %s %s" % (device, fs_dir)}
    ]

    start_time = time.get_time(in_seconds=True)
    for argument in arguments:
        atomic_run(errors=error,
                   **argument)
    end_time = time.get_time(in_seconds=True)
    total_time = time.time_2_sec(end_time - start_time)
    duration.append(total_time)

    return duration, error


def repeated_copy(repeat_count):
    errors = []
    vdostats = VDOStats()
    vdo_name = read_env('fmf_vdo_name')
    device = read_var("VDO_DEVICE")
    fs_dir = read_var("FS_DIR")
    file = read_var("DATA_FILE")

    ret = is_block_device(device)
    if ret != True:
        errors.append(ret)
        return errors

    duration = list()
    i = 0
    while i < repeat_count:
        i += 1
        print("############# Running iteration %s #############" % (i))
        duration, ret = single_copy(vdostats, device, vdo_name, fs_dir, file, duration)
        errors += ret
        print("######### This iteration took %s  #########" % time.sec_2_time(duration[-1]))

        # Reduce iteration count in case the iteration took too long.
        try:
            max_runtime = read_env("fmf_max_runtime")
            avg_duration = sum(duration) / len(duration)
            count = int(max_runtime * 60 / avg_duration)
            if count < repeat_count:
                print("INFO: Changing total amount of iterations from %s to %s to avoid timeout." %
                      (repeat_count, count))
                repeat_count = count
        except KeyError:
            pass

    print("\n####### SUMMARY of %s iterations ########" % (i))
    print("######### Average duration: %s ##########" % time.sec_2_time(int(sum(duration) / len(duration))))
    print("######### Minimum duration: %s ##########" % time.sec_2_time(min(duration)))
    print("######### Maximum duration: %s ##########\n" % time.sec_2_time(max(duration)))
    return errors


if __name__ == "__main__":
    if read_env('fmf_tier') == 1:
        errs = repeated_copy(read_env('fmf_repeat_count'))
    if read_env('fmf_tier') == 2:
        errs = repeated_copy(read_env('fmf_repeat_count'))
    exit(parse_ret(errs))
