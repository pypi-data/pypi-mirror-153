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

"""lsm.py: Module with test specific method for libstoragemgmt."""

from __future__ import absolute_import, division, print_function, unicode_literals
import re
from stqe.host.persistent_vars import read_var, read_env
from stqe.host.fmf_tools import get_env_args


def check_ssl(protocol):
    """
    Checks if fmf_protocol is ssl/no_ssl and limits the protocol by this
    :param protocol:
    :return:
    """
    try:
        ssl = read_env("fmf_protocol")
    except KeyError:
        # Protocol not limited
        return True
    if ssl == "ssl" and "ssl" in protocol or ssl == "no_ssl" and "ssl" not in protocol:
        return True
    return False


def yield_lsm_config():
    config = {
        'protocols': list(),
        'username': None,
        'password': None,
        'target': None
    }

    for conf in config.keys():
        try:
            config[conf] = read_var("LSM_" + conf.upper())
        except IOError:
            pass

    try:
        if not isinstance(config['protocols'], list):
            raise AttributeError
    except AttributeError:
        print("ERROR: Protocols must be list, got %s, type '%s'." % (config['protocols'], type(config['protocols'])))
        exit(1)

    protocols = config.pop('protocols')
    for protocol in protocols:
        if not check_ssl(protocol):
            continue
        config['protocol'] = protocol
        yield config


def get_data_from_script_output(data, id="ID"):
    split_string = re.match("(-*)", data).group()
    try:
        items = [x for x in data.split(split_string) if id in x]
    except ValueError as e:
        print(repr(e))
        return None
    data = dict()
    for item in items:
        for line in item.splitlines():
            if len(line) < 2:
                continue
            if line.startswith(id):
                # luckily ID is always first
                item_id = line.split("|").pop().strip()
                data[item_id] = dict()
            else:
                line_data = line.split("|")
                data[item_id][line_data[0].strip()] = line_data[1].strip()
    return data


def get_local_disk_data(data):
    return get_data_from_script_output(data, id="Path")


def get_id_from_name(data, name, field='Name', item_id="ID"):
    data = get_data_from_script_output(data, id=item_id)
    for line in data:
        if data[line][field] == name:
            return line
    print("FAIL: Could not find item named '%s'." % name)
    return None


def get_data_from_id(data, name, field='Name', item_id="ID"):
    data = get_data_from_script_output(data, id=item_id)
    for line in data:
        if line != name:
            continue
        return data[line][field]
    print("FAIL: Could not find item named '%s'." % name)
    return None


def get_ag_id_from_name(data, name):
    return get_id_from_name(data, name)


def get_fs_id_from_name(data, name):
    return get_id_from_name(data, name)


def get_vol_id_from_name(data, name):
    return get_id_from_name(data, name)


def get_export_id_from_export_path(data, export_path):
    # policy is 'disabled' but cli takes 'disable'
    return get_id_from_name(data, export_path, field="Export Path")


def get_system_read_pct_of_sys(data, sys):
    return get_data_from_script_output(data)[sys]['Read Cache Percentage']


def get_cache_policy_from_id(data, vol_id, field):
    return translate_cache_policy(get_data_from_id(data, vol_id, field=field, item_id="Volume ID"))


def translate_cache_policy(policy):
    dictionary = {"Write Back": "WB",
                  "Write Through": "WT",
                  "Auto": "AUTO",
                  "Enabled": "enable",
                  "Disabled": "disable"}
    try:
        return dictionary[policy]
    except KeyError:
        return policy


def get_replace_dict():
    """
    Returns dict of keys to replace from fmf to libsan.host.lsm.LibStorageMgmt
    :return: dict
    """
    return {"ag_name": 'name',
            "vol_name": 'name',
            "fs_name": 'name',
            "snap_name": 'name',
            "rep_name": 'name'}


def get_lsm_args(lsm_object):
    """
    Returns dict of arguments passed from FMF env vars
    :return: dict
    """
    arguments = dict(lsm_object.arguments)
    # "name" has to be removed, as name is FMF name of the test at this point
    del (arguments["name"])
    return get_env_args(list(arguments) + list(get_replace_dict()),
                        read_var("FILE_NAMES"),
                        get_replace_dict())
