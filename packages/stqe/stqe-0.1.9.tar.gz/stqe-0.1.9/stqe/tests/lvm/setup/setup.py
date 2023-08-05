#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.fmf_tools import get_env_args, read_env, get_func_from_string
from stqe.host.persistent_vars import write_var, read_var
from libsan.host.linux import run
from libsan.host.lvm import lv_create, lv_deactivate, lv_convert
from libsan.host.dmpd import DMPD
from stqe.host.lvm import get_dmpd_args


def mount_lv(vg_name, lv_name):
    """
    Creates dir, filesystem and mounts LV. The purpose of this is to increase metadata volume.
    :param vg_name: VG with LV in it
    :type vg_name: string
    :param lv_name: LV name to be mounted
    :type lv_name: string
    :return: retcode
    :rtype: int
    """
    ret = run("mkdir -p /mnt/%s" % lv_name, verbose=True)
    ret += run("mkfs.ext4 /dev/%s/%s" % (vg_name, lv_name), verbose=True)
    ret += run("mount /dev/%s/%s /mnt/%s/" % (vg_name, lv_name, lv_name), verbose=True)
    return ret


def umount_lv(lv_name):
    """
    Umounts LV and removes dir.
    :param lv_name: mounted LV name
    :type lv_name: string
    :return: retcode
    :rtype: int
    """
    ret = run("umount -f /mnt/%s/" % lv_name, verbose=True)
    ret += run("rm -rf /mnt/%s" % lv_name, verbose=True)
    return ret


def metadata_snapshot(vg_name, thinpool):
    """
    Creates metadata snapshot of thinpool
    :param vg_name: VG with thinpool in it
    :type vg_name: string
    :param thinpool: thinpool name
    :type thinpool: string
    :return: retcode
    :rtype: int
    """
    ret = run("dmsetup suspend /dev/mapper/%s-%s-tpool" % (vg_name, thinpool), verbose=True)
    ret += run("dmsetup message /dev/mapper/%s-%s-tpool 0 reserve_metadata_snap" % (vg_name, thinpool), verbose=True)
    ret += run("dmsetup resume /dev/mapper/%s-%s-tpool" % (vg_name, thinpool), verbose=True)
    return ret


def create_lvs(vg_name, thinpool, lv_name, options, number_of_vols, return_output=True):
    """
    Creates few LVs to fill in pool metadata. This increases transaction ID and allows to do thin_delta
    :param vg_name: VG with thinpool in it
    :type vg_name: string
    :param thinpool: thinpool name
    :type thinpool: string
    :param lv_name: base of LVs name
    :type lv_name: string
    :param options: LV options to be used for creating LVs
    :type options: list
    :param number_of_vols: Number of LVs to create
    :type number_of_vols: int
    :param return_output: should just errors or also retcode? (default True - both)
    :type return_output: bool
    :return: retcode, list of errors
    :rtype: tuple
    """
    errors = []
    for i in range(number_of_vols):
        atomic_run("Creating thin LV No. %s" % i,
                   vg_name=vg_name + "/" + thinpool,
                   lv_name=lv_name + str(i),
                   options=options,
                   command=lv_create,
                   errors=errors)

        atomic_run("Mounting LV No. %s" % i,
                   expected_ret=0,
                   vg_name=vg_name,
                   lv_name=lv_name + str(i),
                   command=mount_lv,
                   errors=errors)

        atomic_run("Unmounting LV No. %s" % i,
                   expected_ret=0,
                   lv_name=lv_name + str(i),
                   command=umount_lv,
                   errors=errors)

        atomic_run("Deactivating thin LV No. %s" % i,
                   vg_name=vg_name,
                   lv_name=lv_name + str(i),
                   command=lv_deactivate,
                   errors=errors)
    if return_output:
        if errors == list():
            return 0, errors
        return 1, errors
    else:
        return errors


def swap_metadata(vg_name, thinpool, lv_swap, return_output=True):
    """
    Swaps thinpool metadata to another LV
    :param vg_name: VG with both thinpool and swap LV in it
    :type vg_name: string
    :param thinpool: thinpool to swap metadata from
    :type thinpool: string
    :param lv_swap: LV to swap metadata to
    :type lv_swap: string
    :param return_output: should just errors or also retcode? (default True - both)
    :type return_output: bool
    :return: retcode, list of errors
    :rtype: tuple
    """
    errors = list()
    atomic_run("Deactivating pool",
               vg_name=vg_name,
               lv_name=thinpool,
               command=lv_deactivate,
               errors=errors)

    atomic_run("Deactivating swap",
               vg_name=vg_name,
               lv_name=lv_swap,
               command=lv_deactivate,
               errors=errors)

    atomic_run("Swapping metadata",
               vg_name=vg_name,
               lv_name=lv_swap,
               options=["-y", "--thinpool %s/%s --poolmetadata" % (vg_name, thinpool)],
               command=lv_convert,
               errors=errors)
    if return_output:
        if errors == list():
            return 0, errors
        return 1, errors
    else:
        return errors


def write_data(args, errors):
    """
    Function for writing persistent var files
    :param args: any arguments supplied to general function
    :type args: dict
    :param errors: list of errors
    :type errors: list
    :return: errors
    :rtype: list
    """
    name = read_env("fmf_name")

    if "create_loopdev" in name:
        atomic_run("Writing var %s" % args['name'].upper(),
                   command=write_var,
                   var={"%s" % args['name'].upper(): "/dev/%s" % args['name']},
                   errors=errors)
        atomic_run("Writing var %s_SIZE" % args['name'].upper(),
                   command=write_var,
                   var={"%s_SIZE" % args['name'].upper(): args['size']},
                   errors=errors)

    if "create_vg" in name:
        atomic_run("Writing var VG_NAME",
                   command=write_var,
                   var={'VG_NAME': args['vg_name']},
                   errors=errors)

    if "create_lv" in name:
        atomic_run("Writing var %s" % args['lv_name'].upper(),
                   command=write_var,
                   var={args['lv_name'].upper(): args['lv_name']},
                   errors=errors)

    if "backup_metadata" in name:
        atomic_run("Writing var METADATA_BACKUP",
                   command=write_var,
                   var={'METADATA_BACKUP': args['output']},
                   errors=errors)
    return errors


def create_loopdev(**kwargs):
    """
    :param kwargs: all args taken by libsan.host.loopdev.create_loopdev
    :type kwargs: dict
    :return: return of libsan.host.loopdev.create_loopdev / None if fail
    :rtype: str / None
    """
    from libsan.host.loopdev import create_loopdev
    from libsan.host.linux import get_free_space
    from os import path

    possible_image_paths = read_env("fmf_possible_image_paths")
    image_path = None

    for possible_path in possible_image_paths:
        # check if the destination exists
        if not path.exists(possible_path):
            print("INFO: path '%s' does not exists, skipping." % possible_path)
            continue
        # comparing MB
        if (float(get_free_space(possible_path)) / 1024 ** 2) > kwargs['size']:
            image_path = possible_path
            break

    return create_loopdev(image_path=image_path, **kwargs) if image_path else None


def setup():
    """
    Basic function to merge it all together
    :return: errors
    :rtype: list
    """
    errors = []
    class_instance = DMPD()
    args = get_dmpd_args(dmpd_object=class_instance)
    args.update(get_env_args(
            {"loop_name": str, "size": int, "pv_name": str, "vg_name": str, "lv_name": str, "lv_swap": str, "path": str,
             "options": list, "number_of_vols": int, "thinpool": str, "source_vg": str, "source_lv": str,
             "source_file": str, "cmd": str, "new_name": str},
            read_var("FILE_NAMES"),
            {"loop_name": "name"}))

    command = args.pop('command')

    args['command'] = get_func_from_string(class_instance, command, local_functions=globals())
    atomic_run(errors=errors,
               **args)

    write_data(args, errors)

    return errors


if __name__ == "__main__":
    errs = setup()
    exit(parse_ret(errs))
