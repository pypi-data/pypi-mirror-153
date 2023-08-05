#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.vdo import VDO
from stqe.host.atomic_run import atomic_run, parse_ret, Logger
from stqe.host.vdo import get_vdo_args, minimum_slab_size, get_underlying_device
from stqe.host.fmf_tools import get_env_args, read_env, get_func_from_string
from stqe.host.persistent_vars import write_var, read_var
from libsan.host.linux import run
import subprocess
import time
import signal
from functools import partial


def write_data(args, errors, extra):
    name = read_env("fmf_name")

    if "create_vdo" in name or ("create/success" in name):
        old_device = read_var('VDO_DEVICE')
        if old_device:
            previous_devices = read_var('VDO_OLD_DEVICES')
            if previous_devices:
                previous_devices.append(old_device)
            else:
                previous_devices = [old_device]
            atomic_run("Writing var VDO_OLD_DEVICES with previous devices.",
                       command=write_var,
                       var={'VDO_OLD_DEVICES': previous_devices},
                       errors=errors)
        else:
            print("INFO: Did not find any previous device.")

        atomic_run("Replacing var VDO_DEVICE with newly created device.",
                   command=write_var,
                   var={'VDO_DEVICE': "/dev/mapper/%s" % args["name"]},
                   errors=errors)

    if "remove_vdo" in name and extra["device"]:
        if len(extra['previous_devices']) > 0:
            atomic_run("Writing var VDO_OLD_DEVICES with previous devices.",
                       command=write_var,
                       var={'VDO_OLD_DEVICES': extra['previous_devices']},
                       errors=errors)
        atomic_run("Replacing var VDO_DEVICE with underlying device.",
                   command=write_var,
                   var={'VDO_DEVICE': extra["device"]},
                   errors=errors)

    if "create_vg" in name:
        atomic_run("Writing var VG_NAME",
                   command=write_var,
                   var={'VG_NAME': args['vg_name']},
                   errors=errors)

    if "mkdir" in name:
        atomic_run("Writing var FS_DIR",
                   command=write_var,
                   var={'FS_DIR': args['cmd'].split()[-1]},
                   errors=errors)

    if "create_lv" in name:
        atomic_run("Writing var %s" % args['lv_name'].upper(),
                   command=write_var,
                   var={args['lv_name'].upper(): args['lv_name']},
                   errors=errors)

    if all([True if x in name else False for x in ["create", "data", "file"]]):
        atomic_run("Writing var DATA_FILE",
                   command=write_var,
                   var={"DATA_FILE": args['cmd'].split("of=")[1].split()[0]},
                   errors=errors)

    # The DM table might be left over, better ensure it is removed now
    if "setup/remove_vdo" in read_env("fmf_name"):
        sleep_time = 60
        atomic_run("Sleeping for %s seconds" % sleep_time, command=time.sleep, secs=sleep_time, errors=errors)
        atomic_run("Checking device mapper table", command=run, cmd="dmsetup table", errors=errors)
        atomic_run("Checking /dev/mapper dir.", command=run, cmd="ls -la /dev/mapper", errors=errors)
        atomic_run("Removing DM device.", command=run, cmd="dmsetup remove %s" % args['name'], errors=[])

    return


def interrupt_command(message, command_string, kill_delay):
    logger = Logger()
    logger.info("%s, command: '%s'." % (message, command_string))
    p = subprocess.Popen(command_string, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    time.sleep(kill_delay)
    p.send_signal(signal.SIGINT)

    # Print the whole stdout and stderr
    out = ""
    err = ""
    for o in iter(partial(p.stdout.readline), b""):
        out += o.decode('ascii', 'ignore') if isinstance(o, bytes) else o
    for e in iter(partial(p.stderr.readline), b""):
        err += e.decode('ascii', 'ignore') if isinstance(e, bytes) else e
    print(out)
    logger.info("Killed the process after delay %ss" % kill_delay)
    print(err)

    time.sleep(5)
    return


def call_func(args, command, errors):
    extra = dict()
    if command == "create":
        args['message'] += " %s." % args['device']

    if "slab_size" in args and args["slab_size"] == "minimum":
        args['slab_size'] = minimum_slab_size(args['device'], default_to_2g=False)

    if command == "remove":
        previous_devices = read_var('VDO_OLD_DEVICES')
        if previous_devices:
            extra['device'] = previous_devices.pop()
            extra['previous_devices'] = previous_devices
        else:
            extra['device'] = get_underlying_device(args['name'])
            extra['previous_devices'] = []
        if not extra['device']:
            print("WARN: Could not find underlying device.")

    if command == "libsan.host.lvm.vg_create" or command == "libsan.host.lvm.lv_create":
        # need to rescan cache when working with lvm, VDO is not good at it.
        atomic_run("Rescanning cache",
                   command=run,
                   cmd="pvscan --cache",
                   errors=errors)

    if command == "libsan.host.lvm.lv_create":
        # Need to recalculate size if given -V X%FREE
        for i, option in enumerate(args['options']):
            if "%" not in option:
                continue
            pct = option.split("%")[0].split()[1]
            ret, data = atomic_run(message="Getting thinpool size.",
                                   command=run,
                                   cmd="lvs %s --noheadings --o size --units g" % args['vg_name'],
                                   return_output=True,
                                   errors=errors)
            try:
                args['options'][i] = "-V %sG " % ((float(pct) / 100) * float(data.strip()[:-1]))
            except ValueError as e:
                print(e)
                print("DEBUG: Got '%s' from command as data." % data)

    if command == "libsan.host.lvm.pv_remove":
        if args["pv_name"].startswith("/dev/mapper"):
            # need to get device in format /dev/vg/lv, format dm-X causes issues with pvremove libsan func
            ret, data = run("ls -la /dev/mapper | grep %s" % args["pv_name"].split("/").pop(), return_output=True)
            if data:
                device = data.split("->")[0].split().pop().strip().split("/").pop().replace("--", "-").split("-")
                if len(device) == 2:
                    args["pv_name"] = "/dev/%s/%s" % ("-".join(device[:-1]), device[-1])

    return extra


def setup():
    errors = []

    vdo = VDO(disable_check=True)
    args = get_vdo_args(vdo_object=vdo)

    # some extra args for some setups
    args.update(get_env_args(["prefix", "pv_name", "vg_name", "lv_name", "options", "cmd", "path",
                              "kill_delay", "command_string"],
                             read_var("FILE_NAMES")))

    command = args.pop('command')

    extra = call_func(args, command, errors)

    if command == "interrupt_command":
        def complete_command_string(cmd, args):
            cmd_string = cmd.pop(0)
            for param in cmd:
                param = param.split("=")
                cmd_string += " %s=%s" % (param[0], args[param[1]])
            return cmd_string

        command_string = complete_command_string(args["command_string"], args)
        interrupt_command(args["message"], command_string, args["kill_delay"])
    else:
        args['command'] = get_func_from_string(vdo, command)
        atomic_run(errors=errors,
                   **args)

    write_data(args, errors, extra)

    return errors


if __name__ == "__main__":
    errs = setup()
    exit(parse_ret(errs))
