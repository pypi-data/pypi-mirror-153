from __future__ import absolute_import, division, print_function, unicode_literals

# Copyright (C) 2018 Red Hat, Inc.
# python-stqe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-stqe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-stqe.  If not, see <http://www.gnu.org/licenses/>.

"""vdo.py: Module with test specific method for VDO."""

from stqe.host.atomic_run import atomic_run
from difflib import context_diff
from libsan.host.cmdline import run
import os
import stat
from stqe.host.fmf_tools import get_env_args
from stqe.host.persistent_vars import read_var
from libsan.host.vdo import VDO
from libsan.host.linux import get_memory


def restart_modify(vdo_object, vdo_name, errors):
    # sometimes VDO needs to be restarted for changes to take effect
    print("Restarting VDO for changes to take effect.")
    commands = [
        {'message': "Stopping VDO to apply modification.", 'command': vdo_object.stop,
         'expected_out': ["Stopping VDO"]},
        {'message': "Starting VDO to apply modification.", 'command': vdo_object.start,
         'expected_out': ["Starting VDO", "VDO instance", "is ready"]}
    ]
    for command in commands:
        atomic_run(name=vdo_name,
                   errors=errors,
                   expected_ret=0,
                   **command)
    return


def report_modify_difference(errors, status_old, status_new, changed_var, changed_argument):
    status_old = [x for x in status_old.splitlines() if changed_var in x]
    status_new = [x for x in status_new.splitlines() if changed_var in x]
    print("Before: %s" % ", ".join(status_old))
    print("After:  %s" % ", ".join(status_new))
    diff = list(context_diff(status_old, status_new))
    difference = "\n".join([x for x in diff if x.startswith("!")])

    if difference == "":
        error = 'WARN: Modifying VDO to %s did nothing.' % changed_argument
        print(error)
        errors.append(error)
    return


def minimum_slab_size(device, default_to_2g=True):
    def _get_raid_device(device):
        device_name = device.split("/").pop()
        ret, device_link = run(cmd="ls -al /dev/md | grep %s" % device_name, return_output=True)
        if ret or device_link is None:
            print("WARN: Device %s not found in /dev/md." % device_name)
            return None
        raid_device = device_link.split("../").pop()
        return raid_device

    if device.startswith("/dev/md"):
        device_name = _get_raid_device(device)
    else:
        device_name = device.split("/").pop()
    ret, device_size = run(cmd="lsblk | grep '%s ' " % device_name, return_output=True)
    if ret or device_size is None:
        print("WARN: Device %s not found using lsblk. Using default 2G size." % device_name)
        return "2G"
    size = device_size.split()[3]
    multipliers = ["M", "G", "T", "P", "E"]
    device_size = (float(size[:-1]) * (1024 ** multipliers.index(size[-1:]))).__int__()
    max_number_of_slabs = 8192
    minimum_size = 2 ** int((device_size / max_number_of_slabs)).bit_length()
    if minimum_size < 128:
        minimum_size = 128
    if default_to_2g and minimum_size < 2048:
        return "2G"
    return str(minimum_size) + "M"


def maximum_logical_size():
    """
    Returns maximum logical size based on memory
    :return: string max_size
    """
    memory = get_memory()['mem']['free']
    size = '4096T'
    if memory < 10000:
        size = 2 ** (((4096.0 / 10000) * float(memory)).__int__().bit_length() - 1)
        if size > 4096:
            size = 4096
        size = str(size) + 'T'
    return size


def is_block_device(device):
    try:
        mode = os.stat(device).st_mode
    except OSError:
        msg = "Device %s does not exist." % device
        return msg

    if not stat.S_ISBLK(mode):
        msg = "Device %s is not block device, aborting." % device
        print(msg)
        return msg
    return True


def get_underlying_device(name, conf_file="/etc/vdoconf.yml"):
    vdo = VDO(disable_check=True)
    ret, data = vdo.status(name=name, return_output=True, verbosity=False, conf_file=conf_file)
    if ret != 0:
        msg = "FAIL: Could not get status of VDO device '%s'." % name
        print(msg)
        return None
    device = None
    for line in data.splitlines():
        if 'Storage device' in line:
            device = "/dev/%s" % line.split("/dev/").pop().split().pop(0).strip()
    if device is None:
        # The device is probably crashed and needs to be force removed
        print("WARN: Could not find 'Device mapper status' in vdo status output.")
        # Let's try alternative way of getting the device by checking vdo config file
        # First get the config file
        conf_file = None
        for line in data.splitlines():
            if "File:" in line:
                conf_file = line.split("File:").pop().strip()
        if not conf_file:
            print("FAIL: Could not find vdo conf file in vdo status, something is really wrong!")
            return None
        # Read the file contents
        with open(conf_file) as f:
            lines = f.readlines()
        correct_vdo_device = False
        for line in lines:
            if "%s:" % name in line:
                # Get the correct VDO device in the config, there might be more
                correct_vdo_device = True
            if correct_vdo_device and "device:" in line:
                # Now we have the device, just need to follow the link
                device = line.split("device:").pop().strip()
                break

    # now we might have /dev/disk/by-id/UUID, need to get something reasonable
    _, data = run("ls -la %s" % device, return_output=True, verbose=False)
    device = data.split("/").pop().strip()

    # format dm-X causes issues later on, where the device cannot be found using lsblk to check for size
    if device.startswith("dm-"):
        with open("/sys/block/%s/dm/name" % device) as f:
            dev_name = f.readline().rstrip('\n')
        device = "/dev/mapper/%s" % dev_name
    else:
        device = "/dev/%s" % device

    return device


def get_replace_dict():
    """
    Returns dict of keys to replace from fmf to libsan.host.vdo.VDO
    :return: dict
    """
    return {"vdo_name": 'name'}


def get_vdo_args(vdo_object):
    """
    Returns dict of arguments passed from FMF env vars
    :return: dict
    """
    arguments = dict(vdo_object.arguments)
    # "name" has to be removed, as name is FMF name of the test at this point
    del (arguments["name"])
    return get_env_args(list(arguments) + list(get_replace_dict()) + ["grow_type"],
                        read_var("FILE_NAMES"),
                        get_replace_dict())
