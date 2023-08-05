from __future__ import absolute_import, division, print_function, unicode_literals

# Copyright (C) 2016 Red Hat, Inc.
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

"""persistent_vars.py: Module to share variables between scripts using writing to file."""

import os
from libsan.host.cmdline import run


def get_persistent_files_dir():
    """
    :return: Directory of persistent vars.
    :rtype: string
    """
    return "/tmp/"


def get_persistent_vars_file_name():
    """
    :return: File name of persistent vars file.
    :rtype: string
    """
    return "FILE_NAMES"


def exists_persistent_vars_file():
    """
    :return: True if persistent vars filer exists, default /tmp/FILE_NAMES
    :rtype: bool
    """
    return os.path.exists(get_persistent_files_dir() + get_persistent_vars_file_name())


def _check_0_start(value):
    """
    Checks if value starts with 0 but is not 0. This prevents from changing '02314' but allows changing '0'
    :param value: value to check
    :type value: string
    :return: True if starts with 0 and is not 0, False otherwise
    :rtype: bool
    """
    return all([value.startswith("0"), not value == "0"])


def _read_to_float(value):
    """
    :param value: Value to try to change to float
    :type value: any, preferable string
    :return: (False, original value) or (True, float(value))
    :rtype: tuple
    """
    try:
        return (True, float(value)) if not all([_check_0_start(value), not value.startswith("0.")]) else (False, value)
    except ValueError:
        return False, value


def _read_to_int(value):
    """
    :param value: Value to try to change to integer
    :type value: any, preferable string
    :return: (False, original value) or (True, int(value))
    :rtype: tuple
    """
    try:
        return (True, int(value)) if not _check_0_start(value) else (False, value)
    except ValueError:
        return False, value


def _read_to_list(value):
    """
    This does not support nested lists!
    :param value: Value to try to change to list
    :type value: any, preferable string
    :return: (False, original value) or (True, list(value))
    :rtype: tuple
    """
    try:
        if value.startswith("["):
            return True, value[1:-1].split(", ")
        return False, value
    except AttributeError:
        return False, value


def _read_to_none(value):
    """
    :param value: Value to try to change to None
    :type value: any, preferable string
    :return: (False, original value) or (True, None)
    :rtype: tuple
    """
    if value == str(None):
        return True, None
    return False, value


def _read_to_bool(value):
    """
    Checks if value is "true" or "false" string, returns bool equivalent.
    :param value: Value to try to change to bool
    :type value: any, preferable string
    :return: (False, original value) or (True, True/False)
    :rtype: tuple
    """
    if value.lower() == "true":
        return True, True
    elif value.lower() == "false":
        return True, False
    return False, value


def _remove_quotes(value):
    """
    Removes any characters ' or " from any string
    :param value: Value to remove quotes from
    :type value: string
    :return: original string without quotes
    :rtype: string
    """
    return "".join([char for char in value if char not in ["\'", "\""]])


def recursive_read_value(value):
    """
    Given string tries to change type of the string to different types. Returns value of new type of possible.
    Supported new types: list, int, float, None, bool
    Example: str("21654") changes to int(21654)
    :param value: value to be retyped
    :type value: string
    :return: value of new type
    :rtype: any(string, list, int, float, None, bool)
    """
    value = _remove_quotes(value)
    for func in [_read_to_list, _read_to_int, _read_to_float, _read_to_none, _read_to_bool]:
        ret, value = func(value)
        if ret:
            if func == _read_to_list:
                return [recursive_read_value(val) for val in value]
            return value
    return value


def read_var(var):
    """
    :param var: variable name saved in file of the same name in get_persistent_files_dir() location
    :type var: string
    :return: Value saved in the file with proper type
    :rtype: any(_recursive_read_value)
    """
    if not os.path.isfile(get_persistent_files_dir() + var):
        if var != get_persistent_vars_file_name():
            print("FAIL: File %s does not exist." % (get_persistent_files_dir() + var))
        return None
    with open(get_persistent_files_dir() + var, 'r') as f:
        value = f.read()
    return recursive_read_value(value)


def read_env(var):
    """
    This does not handle KeyError, it is intentional.
    :param var: os.environ variable
    :type var: string
    :return: value of environ variable
    :rtype: any(_recursive_read_value)
    """
    return recursive_read_value(os.environ[var])


def _write_to_string(value):
    """
    :param value: Value to try to change to string
    :type value: any
    :return: (False, original value) or (True, str(value))
    :rtype: tuple
    """
    try:
        return True, str(value)
    except ValueError:
        return False, value


def _write_from_list(value):
    """
    :param value: Value to try to change to list
    :type value: list
    :return: (False, original value) or (True, str(list(value)) without '' or "")
    :rtype: tuple
    """
    if isinstance(value, list):
        return True, "[%s]" % ", ".join([str(x) for x in value[:]])
    return False, value


def write_var(var):
    """
    :param var: variable to write to file in format {var_name: var_value}
    :type var: dict
    :return: 0 pass, 1 fail
    :rtype: int
    """
    if not isinstance(var, dict):
        print("FAIL: var manipulation requires var as a dict. {name: value}")
        return 1
    file_name = list(var.keys()).pop()
    write_file(file_name, list(var.values()).pop())
    add_file_to_list(file_name)
    return 0


def write_file(file_name, value):
    """
    :param file_name: File name to write to location get_persistent_files_dir() + file_name
    :type file_name: string
    :param value: value to write to the file
    :type value: dict
    :return: None
    :rtype: None
    """
    with open(get_persistent_files_dir() + file_name, 'w') as f:
        for func in (_write_from_list, _write_to_string):
            ret, value = func(value)
            if ret:
                break
        f.write(value)


def add_file_to_list(file_name):
    """
    This is for adding file names to persistent list so we can clean them later.
    :param file_name: name of the persistent vars file
    :type file_name: string
    :return: None
    :rtype: None
    """
    file_names = read_var(get_persistent_vars_file_name()) or []
    if file_name not in file_names:
        file_names.append(file_name)
    write_file(get_persistent_vars_file_name(), file_names)


def clean_var(var):
    """
    Cleans persistent var file from filesystem
    :param var: variable name to clean
    :type var: string
    :return: 0
    :rtype: int
    """
    os.remove(get_persistent_files_dir() + var)
    return 0


def clean_all_vars(prefix=""):
    """
    This uses list of persistent vars files from get_persistent_files_dir() and get_persistent_vars_file_name() and
    cleans them from filesystem.
    :param prefix: prefix to clean only some, for example "LSM_"
    :type prefix: string
    :return: 0
    :rtype: int
    """
    prefix = prefix or ""
    variables = get_persistent_var_names(prefix)
    if exists_persistent_vars_file() and get_persistent_vars_file_name() not in variables:
        variables.append(get_persistent_vars_file_name())
    print("INFO: Will clean these variables: \n\t%s" % "\n\t".join(variables))
    for var in variables:
        clean_var(var)
    return 0


def get_persistent_var_names(prefix=""):
    """
    Gets persistent vars from get_persistent_vars_file_name() file or filesystem in get_persistent_files_dir() location
    :param prefix: prefix to clean only some, for example "LSM_"
    :type prefix: string
    :return: List of persistent vars file names having the specified prefix
    :rtype: list
    """
    if exists_persistent_vars_file():
        variables = read_var(get_persistent_vars_file_name())
    else:
        _, variables = run("ls -la %s" % get_persistent_files_dir(), return_output=True, verbose=False)
        variables = [line.split().pop() for line in variables.splitlines()[3:]]
    return [value for value in variables if value.startswith(prefix)]
