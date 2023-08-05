#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.vdo import VDO
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_env, read_var, write_var
from stqe.host.vdo import get_vdo_args, minimum_slab_size, maximum_logical_size, restart_modify, \
    report_modify_difference, get_underlying_device
from stqe.host.fmf_tools import get_env_args, get_func_from_string


def requires_restart_after_modification():
    return list(modification_args())


def modification_args(command=False):
    if command:
        return {"compression": "Compression",
                "deduplication": "Deduplication",
                "activate": "Activate",
                "deactivate": "Activate",
                "change_write_policy": "Configured write policy",
                "start": "Device mapper status",
                "stop": "Device mapper status",
                "grow": "size"}
    return {"ack_threads": "Acknowledgement threads",
            "bio_rotation_interval": "Bio rotation interval",
            "bio_threads": "Bio submission threads",
            "block_map_cache_size": "Block map cache size",
            "block_map_period": "Block map period",
            "cpu_threads": "CPU-work threads",
            "hash_zone_threads": "Hash zone threads",
            "logical_threads": "Logical threads",
            "max_discard_size": "Max discard size",
            "physical_threads": "Physical threads"}


def commands_changing_stats():
    return ["compression", "deduplication", "activate", "deactivate", "change_write_policy", "stop", "start", "grow"]


def list_not_changing(**kwargs):
    from libsan.host.lvm import lv_create, lv_remove

    def _create_lvs(vg, count, errors):
        for i in range(count):
            atomic_run("Creating LV lv%s" % i,
                       command=lv_create,
                       lv_name="lv%s" % i,
                       vg_name=vg,
                       options=["-l %s%%VG" % int(100 / count)],
                       errors=errors)
        print("INFO: All LVs created.")

    def _remove_lvs(vg, count, errors):
        for i in range(count):
            atomic_run("Removing LV lv%s" % i,
                       command=lv_remove,
                       lv_name="lv%s" % i,
                       vg_name=vg,
                       errors=errors)
        print("INFO: All LVs removed.")

    def _create_vdos(vdo, vg, count, errors):
        for i in range(count):
            atomic_run("Creating VDO vdo%s" % i,
                       command=vdo.create,
                       name="vdo_list%s" % i,
                       device="/dev/mapper/%s-lv%s" % (vg, i),
                       slab_size=minimum_slab_size("/dev/mapper/%s-lv%s" % (vg, i), default_to_2g=False),
                       errors=errors)
        print("INFO: All VDOs created.")

    def _remove_vdos(vdo, count, errors):
        for i in range(count):
            atomic_run("Removing VDO vdo%s" % i,
                       command=vdo.remove,
                       force=True,
                       name="vdo_list%s" % i, errors=errors)
        print("INFO: All VDOs removed.")

    errors = []

    vg = read_var("VG_NAME")
    _create_lvs(vg, kwargs["count"], errors)

    vdo = VDO(disable_check=True)
    _create_vdos(vdo, vg, kwargs["count"], errors)
    x = ""
    ret = 0
    vdo = VDO(disable_check=True)
    for i in range(kwargs["iterations"]):
        print("I: %s" % i)
        _, y = vdo.list(return_output=True)
        if i == 0:
            x = y
            continue
        if x != y:
            ret = 1
            e = "##### DIFFERENT LISTINGS, iteration %s #####\n" % i
            e += "X: %s\n" % x
            e += "#####\n"
            e += "Y: %s\n" % y
            errors.append(e)
            break
    out = "Checking listing passed %s iterations." % kwargs["iterations"] if errors == [] else "/n".join(errors)
    _remove_vdos(vdo, kwargs["count"], errors)
    _remove_lvs(vg, kwargs["count"], errors)
    print(out, type("out"))
    return ret, out


def grow_physical(return_output=True):
    from libsan.host.lvm import lv_extend
    errors = []
    lv = read_var("LV_THIN")
    vg = read_var("VG_NAME")
    vdo = VDO(disable_check=True)
    min_slab_size = minimum_slab_size("/dev/mapper/%s-%s" % (vg, lv), default_to_2g=False)
    arguments = [
        {'message': "Creating VDO to be grown", 'command': vdo.create, 'name': "vdo_grow",
         'device': "/dev/mapper/%s-%s" % (vg, lv), 'force': True, 'slab_size': min_slab_size},
        {'message': "Growing LV under VDO to have extra physical size", 'command': lv_extend, 'vg_name': vg,
         'lv_name': lv, 'options': ['-L +%s' % (str(int(min_slab_size[:-1]) * 3) + "M")]},
        {'message': "Growing physical size", 'command': vdo.grow, 'grow_type': "physical", 'name': "vdo_grow"},
        {'message': "Removing VDO device", 'command': vdo.remove, 'name': "vdo_grow"}
        # TODO: Reduce the LV to original size
    ]
    ret = 0
    for argument in arguments:
        ret_cycle = atomic_run(errors=errors,
                               **argument)
        if ret_cycle != 0:
            ret = 1
    return (ret, "/n".join(errors)) if return_output else ret


def call_func(args, vdo_object, errors):
    # slab size checking
    if "create" in read_env("fmf_name") and "success" in read_env("fmf_name") and "slab_size" not in args:
        args["slab_size"] = minimum_slab_size(args['device'])
        if args["slab_size"] == "2G":
            # 2G is default, no need to specify it
            args.pop('slab_size')

    if "slab_size" in args and args['slab_size'] == "minimum":
        args["slab_size"] = minimum_slab_size(args['device'], default_to_2g=False)

    if "logical_size" in args and args['logical_size'] == "maximum":
        args['logical_size'] = maximum_logical_size()

    if ("vdo_cli/modify" in read_env("fmf_name") or "vdo_cli/various_commands" in read_env("fmf_name")) and \
            "success" in read_env("fmf_name"):
        extra_args = {"name": args['name']} if "name" in args else {}
        extra_args = {"conf_file": args['conf_file']} if "conf_file" in args else extra_args
        _, args["status_before"] = atomic_run("Getting VDO status after modifications",
                                              return_output=True,
                                              verbosity=False,
                                              command=vdo_object.status,
                                              errors=errors,
                                              **extra_args)

    if "various_commands/remove/success" in read_env("fmf_name"):
        device = get_underlying_device(name=args["name"],
                                       conf_file=args["conf_file"] if "conf_file" in args else "/etc/vdoconf.yml")
        if device:
            atomic_run("Replacing var VDO_DEVICE with underlying device.",
                       command=write_var,
                       var={'VDO_DEVICE': device},
                       errors=errors)
    return args


def vdo_cli():
    errors = []
    vdo = VDO(disable_check=True)
    args = get_vdo_args(vdo_object=vdo)
    # some extra args for some setups
    args.update(get_env_args({"path": str, "enable": None, "iterations": int, "count": int, "vg_name": None}))

    args = call_func(args, vdo, errors)
    if args is None:
        return errors
    status_before = args.pop("status_before") if "status_before" in args else ""

    command_string = args['command']
    args['command'] = get_func_from_string(vdo, args.pop('command'), local_functions=globals())

    ret = atomic_run(errors=errors,
                     **args)

    check_clean(ret=ret, vdo_object=vdo, args=args, errors=errors, status_before=status_before, command=command_string)

    return errors


def check_clean(**kwargs):
    try:
        if read_env("fmf_requires_restart") == True:
            restart_modify(vdo_object=kwargs["vdo_object"], vdo_name=kwargs["args"]['name'], errors=kwargs["errors"])
    except KeyError:
        pass
    if ("vdo_cli/modify" in read_env("fmf_name") or kwargs["command"] in commands_changing_stats()) and \
            "success" in read_env("fmf_name") and not \
            any([True for x in ["log_file", "conf_file", "verbose"] if x in read_env("fmf_name")]):
        name = {"name": kwargs["args"]['name']} if "name" in kwargs["args"] else {}
        _, status_after = atomic_run("Getting VDO status after change",
                                     return_output=True,
                                     verbosity=False,
                                     command=kwargs["vdo_object"].status,
                                     errors=kwargs["errors"],
                                     **name)
        changed_vars_name = []
        changed_args = []
        is_command = True if kwargs["command"] in commands_changing_stats() else False

        for arg in list(kwargs["args"]) + [kwargs["command"]]:
            if arg in modification_args(is_command):
                changed_vars_name.append(modification_args(is_command)[arg])
                changed_args.append(arg)

        for i, changed_var_name in enumerate(changed_vars_name):
            report_modify_difference(errors=kwargs["errors"], status_old=kwargs["status_before"],
                                     status_new=status_after, changed_var=changed_var_name,
                                     changed_argument=changed_args[i])
    return


if __name__ == "__main__":
    errs = vdo_cli()
    exit(parse_ret(errs))
