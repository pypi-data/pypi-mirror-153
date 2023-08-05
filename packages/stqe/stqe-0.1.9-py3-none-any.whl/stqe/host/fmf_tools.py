# -*- coding: utf-8 -*-
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

"""fmf_tools.py: Module to manipulate FMF."""

import os
import fmf.utils
import copy
import stqe
from fmf import Tree
from random import shuffle
from libsan.host.cmdline import run
from stqe.host.persistent_vars import read_env, read_var, get_persistent_files_dir, get_persistent_vars_file_name

_INSTALL_SCRIPT = """#!/usr/bin/python
from libsan.host.linux import install_package

install_package(pack=, check=False)
"""


class TestNotFound(Exception):
    """Raise when test case could not be found"""
    pass


def remove_nones(kwargs):
    # removes keys from kwargs dict that are Nones
    # returns the same dict without those keys
    return {k: v for k, v in kwargs.items() if v is not None}


def get_stqe_path():
    stqe_path = stqe.__file__
    return stqe_path.replace('__init__.py', '')


def get_dir_from_name(name):
    if not os.path.isdir(get_stqe_path() + "/tests/" + name):
        return "/".join(name.split("/")[:-1])
    return name


def get_tree():
    """
    Returns FMF Tree object initialized in stqe tests root directory.
    :return:
    :rtype Tree
    :return: FMF Tree object with root in stqe tests path
    """
    path = get_stqe_path() + "/tests/"
    return Tree(path)


def get_tests_path(name):
    return get_stqe_path() + "/tests/" + get_dir_from_name(name)


def get_test_name(tree):
    test_path = tree.get('test')
    if test_path.startswith("/"):
        return test_path
    remove, test_path = correct_path(test_path)
    return "/".join(tree.name.split("/")[1:-(1 + remove)]) + "/" + test_path


def correct_path(path):
    # Sometimes there is '../$path' in path, we need get number of these and remove them from the path
    remove = 0
    while "../" in path:
        path = "/".join(path.split("/")[1:])
        remove += 1
    return remove, path


def remove_redundant(leaf):
    for att in ['tester', 'description', 'active', 'requires_install', 'requires_cleanup', 'requires_setup',
                'component', 'storage']:
        try:
            del leaf[att]
        except KeyError:
            pass
    return leaf


def get_tests(tree, name=None, filter=None, os_env_asterix=None, bz=None):
    filter = filter or list("")

    config = {
        "install": [],
        "tests": [],
        "setups": [],
        "test_cleanups": {}
    }

    for i in tree.climb():
        leaf = i.get()

        # Ignore yaml aliases
        if "_alias" in i.name:
            continue

        # do not run deactivated tests
        if bz is None and 'active' in leaf and not leaf['active']:
            continue

        # no file associated with this metadata, skipping
        if 'test' not in leaf:
            continue
        # replace test value with path from stqe/tests
        leaf['test'] = get_test_name(i)

        # TODO: Do not run tests with leaf['bz'] unless asked for (bz is set)
        # Run only tests with given bz number
        if bz is not None and 'setup' not in leaf and \
                ('bz' not in leaf or not any([True for l in leaf['bz'] if l == bz])):
            # print "DEBUG: %s" % leaf['test']
            continue

        test_name = i.name.split("/")
        if len(test_name) > 1:
            leaf['name'] = "/".join(test_name[1:])
        else:
            leaf['name'] = i.name

        # do not run setups / cleanups, they are ran by specifying 'requires_setup' / 'requires_cleanup' in test meta
        # add them to "setups" so we can locate them later without running though the tree again
        if 'setup' in leaf and leaf['setup']:
            config["setups"].append(dict(leaf))

        config["test_cleanups"][leaf['name']] = dict(leaf)
        if 'cleanup' in leaf and leaf['cleanup'] or 'setup' in leaf and leaf['setup']:
            continue

        # skip test that doesn't contain string specified with 'name' parameter
        if name is not None and name not in i.show(brief=True):
            continue

        # apply filter
        if not all([fmf_filter(filter=f, node=dict(leaf)) for f in filter]):
            continue

        config, leaf = insert_install(config, leaf)

        if 'requires_setup' not in leaf:
            # this test does not require setup
            is_in_tests = _is_test_in_tests(leaf['name'], config['tests'])
            if isinstance(is_in_tests, bool) and not is_in_tests:
                config['tests'].append(dict(leaf))
            elif isinstance(is_in_tests, int):
                # replace test if it is greater tier
                config['tests'][is_in_tests] = leaf
            test_position = _get_test_position(leaf['name'], config['tests'])
            try:
                if test_position is not None and leaf['tier'] > config['tests'][test_position]['tier']:
                    # replacing tier with higher one
                    config['tests'][test_position] = leaf
            except KeyError:
                pass
            if not _is_test_in_tests(leaf['name'], config['tests']):
                # test is not in yet
                config['tests'].append(dict(leaf))
        else:
            requires_setup = replace_require_setup(leaf, os_env_asterix)
            config = insert_test(config, requires_setup, leaf)
    return config


def insert_install(tests, leaf):
    # write install test file for each package and adds them to the beginning of tests
    if 'requires_install' not in leaf:
        return tests, leaf
    requires_install = leaf.pop('requires_install')
    if not isinstance(requires_install, list):
        requires_install = [requires_install]
    for to_install in requires_install:
        inst_file = "install_%s.py" % to_install
        if not os.path.isfile(get_stqe_path() + "/tests/" + inst_file):
            with open(get_stqe_path() + "/tests/" + inst_file, 'w') as f:
                script = _INSTALL_SCRIPT.split(',')
                script.insert(1, "'%s'," % to_install)
                # write the inst file itself
                f.writelines("".join(script))
                # write inst file to config to be ran
            # make it executable so it can be ran as a test case
            run("chmod +x %s" % (get_stqe_path() + "/tests/" + inst_file))
        inst = {'test': inst_file, 'name': inst_file, 'install': True}
        inst["test_type"] = "install"
        if inst not in tests['install']:
            tests['install'].insert(0, inst)
    return tests, leaf


def _get_test_position(test, tests):
    for i, t in enumerate(tests):
        if test == t['name']:
            return i
    return None


def _is_test_in_tests(test, tests):
    for i, t in enumerate(tests):
        if test == t['name']:
            return True
    return False


def replace_require_setup(leaf, os_env=None):
    require_setup = leaf.pop('requires_setup')
    # check if the setup requirement needs to be altered (contains "*")
    if not isinstance(require_setup, list):
        require_setup = [require_setup]
    req = ""
    for requirement in require_setup:
        if "*" in requirement:
            if os_env is None:
                print("FAIL: Set '%s' env to specify setup type for tests." % os_env)
                exit(1)
            env = os_env.split()
            # replace '*' with the correct device type and adds the rest setup functions
            req = ""
            for i, x in enumerate(env):
                if i == 0:
                    req += x.join(requirement.split("*"))
                else:
                    req += " " + x
        else:
            req += requirement
        req += " "
    return req


def insert_test(dictionary, name, test):
    name = [x.strip() for x in name.split()]
    if len(name) == 1:
        this_name = name[0]
        name = None
    else:
        this_name = name.pop(0)
        name = " ".join(name)
    if this_name not in dictionary:
        dictionary[this_name] = dict()
        dictionary[this_name]['tests'] = []
    for key in dictionary:
        if isinstance(dictionary[key], dict) and name is not None and key == this_name:
            insert_test(dictionary[key], name, test)
        if name is None and key == this_name:
            test_position = _get_test_position(test['name'], dictionary[key]['tests'])
            try:
                if test_position is not None and test['tier'] > dictionary[key]['tests'][test_position]['tier']:
                    # replacing tier with higher one
                    dictionary[key]['tests'][test_position] = test
            except KeyError:
                pass
            if not _is_test_in_tests(test['name'], dictionary[key]['tests']):
                # test is not in yet
                dictionary[key]['tests'].append(dict(test))
    return dictionary


def fmf_filter(filter, node):
    try:
        return fmf.utils.filter(filter=filter, data=node)
    except fmf.utils.FilterError:
        # If the attribute is missing, return as not found
        return False


def filter_tree(filters, name=None, verbose=False, to_print=False):
    # returns list of tests filtered by given filter
    #         "tier:1 & test:this.py" --> all tests that run 'this.py' on tier 1
    #         "tier:1 | test:this.py" --> all tests that run 'this.py' or are on tier 1
    # verbose True: returns list of dicts of test metadata
    #         False: return list of strings of test names

    if not isinstance(filters, list):
        raise fmf.utils.FilterError("Invalid filter '%s'" % type(filters))
    for f in filters:
        if not isinstance(f, str):
            raise fmf.utils.FilterError("Invalid filter '%s'" % type(f))
    tree = get_tree()
    filtered = []
    for leaf in tree.climb():
        # skip test that doesn't contain string specified with 'name' parameter
        if name is not None and name not in leaf.show(brief=True):
            continue
        try:
            if not all([fmf_filter(filter=f, node=leaf.data) for f in filters]):
                continue
        # Handle missing attribute as if filter failed
        except fmf.utils.FilterError:
            continue
        if not verbose:
            filtered.append(leaf.show(brief=True))
        else:
            if to_print:
                filtered.append(dict(leaf.show()))
            else:
                filtered.append(dict(leaf.data))
    return filtered


def get_config(main_dictionary, dictionary=None, conf=None, sort=False):
    conf = conf or list()
    if dictionary is None:
        dictionary = main_dictionary
    if sort:
        dictionary['tests'].sort(key=lambda x: x['name'])
    else:
        shuffle(dictionary['tests'])
    for test in dictionary['tests']:
        test["test_type"] = "test"
        conf.append(remove_redundant(dict(test)))
        if "requires_cleanup" in test:
            # append all cleanups required for this test
            for test_cleanup in test["requires_cleanup"]:
                test_cleanup = get_test_cleanup(main_dictionary, test_cleanup)
                test_cleanup["test_type"] = "cleanup"
                conf.append(remove_redundant(dict(test_cleanup)))
    for key in dictionary:
        # This is not a test, just a dictionary of containing other tests/setups...
        if key in ['tests', 'install', 'setups', 'test_cleanups']:
            continue
        setup = copy.deepcopy(get_setup(main_dictionary, key))
        setup["test_type"] = "setup"
        cleanup = None
        if 'requires_cleanup' in setup:
            cleanup = setup.pop('requires_cleanup')
        conf.append(remove_redundant(dict(setup)))
        if isinstance(dictionary[key], dict):
            conf = get_config(main_dictionary, dictionary[key], conf, sort=sort)
        if cleanup is not None:
            if not isinstance(cleanup, list):
                cleanup = [cleanup]
            for c in cleanup:
                c = get_setup(main_dictionary, c)
                c["test_type"] = "cleanup"
                conf.append(remove_redundant(dict(c)))
                conf, leaf = insert_install(conf, c)
    if dictionary == main_dictionary:
        for install in main_dictionary['install']:
            conf.insert(0, remove_redundant(install))
    return conf


def get_test_cleanup(dictionary, name):
    if name in dictionary["test_cleanups"]:
        if 'requires_install' in dictionary["test_cleanups"][name]:
            insert_install(dictionary, dictionary["test_cleanups"][name])
        return dictionary["test_cleanups"][name]
    msg = "FAIL: Could not find cleanup %s!" % name + "\nPossible cleanups: \n\t%s" % \
          "\n\t".join(dictionary["test_cleanups"].keys())
    raise TestNotFound(msg)


def get_possible_setups(dictionary, name):
    return ["_".join(x['name'].split("/").pop().split("_")[:]) for x in dictionary if
            "storage" in x and x["storage"] and x['name'].split("/")[:-1] == name.split("/")[:-1]]


def get_setup(dictionary, name):
    for setup in dictionary["setups"]:
        if setup['name'] == name:
            if 'requires_install' in setup:
                insert_install(dictionary, setup)
            return setup
    msg = "FAIL: Could not find setup %s!" % name + "\nPossible setups: \n\t%s" % \
          "\n\t".join(get_possible_setups(dictionary["setups"], name))
    raise TestNotFound(msg)


def get_report(report, main, config, padding="", no_metadata=False, metadata=None):
    metadata = metadata or list(['description', 'tier'])

    def add_metadata(_leaf, _padding, _ending, _metadata):
        data = ""
        if _ending == "└── ":
            _padding += "    "
        else:
            _padding += "│   "

        _ending = "├── "
        for i, item in enumerate(_metadata):
            if i == len(_metadata) - 1:
                _ending = "└── "
            try:
                data += _padding + _ending + "%s: %s" % (item, _leaf[item]) + "\n"
            except KeyError:
                pass
        return data

    def add_name(_name, _padding):
        return _padding + _name + "\n"

    try:
        config.pop("install")
        config.pop("setups")
        config.pop("test_cleanups")
    except KeyError:
        pass

    config["tests"].sort(key=lambda x: x['name'])
    tests = config.pop("tests")
    for t, test in enumerate(tests):
        ending = "├── "
        if t + 1 == len(tests) and len(config) == 0:
            ending = "└── "
        report += add_name("T: " + test["name"], padding + ending)
        if not no_metadata:
            report += add_metadata(test, padding, ending, metadata)

    for s, setup in enumerate(config):
        name = setup
        if "*" not in setup:
            name = get_setup(main, setup)["name"]
        if s + 1 < len(config):
            report += add_name("S: " + name, padding + "├── ")
            ending = "│   "
        else:
            report += add_name("S: " + name, padding + "└── ")
            ending = "    "
        report = get_report(report, main, config[setup], padding + ending, no_metadata, metadata)

    return report


def _replace_env_args_with_persistent(args, persistent):
    """
    Automatically replaces args from environ with persistent values stored in files
    :param args: dict of env args already filled
    :param persistent: list of possible persistent vars
    :return: modified args
    """

    def _is_part_of_longer_persistent_var_name(var):
        # need to check if the persistent var is not just part of some longer persistent var name
        # checks char before and char after
        for char_position in [[0, -1], [1, 0]]:
            try:
                char = var.split(p)[char_position[0]][char_position[-1]]
                if char == "_" or char.isupper() and char.isalpha() or int(char):
                    break
            except (IndexError, ValueError):
                pass
        else:
            # is executed if the for loop exits normally (e.g. not by 'break')
            return False
        return True

    def _replace_value(var):
        # Recursively replaces the variable with persistent name in case of list
        if isinstance(var, list):
            for i, item in enumerate(var):
                var[i] = _replace_value(item)
        else:
            # The value needs to be string, as persistent var files are strings and its name should be in var
            # And since we now know it is a string, we can replace it
            if not isinstance(var, type("")) or p not in var:
                return var
            # The var is exactly what we want to replace, do it
            if p == var:
                return read_var(p)
            # Maybe persistent var name is there, but it is part of longer one, check it before replacing
            if not _is_part_of_longer_persistent_var_name(var):
                var = var.replace(p, str(read_var(p)))
        return var

    if not persistent:
        return args
    for arg in args:
        for p in persistent:
            if args[arg] is None:
                continue
            try:
                # List and Dict are nested, cannot compare this easily
                if not (isinstance(args[arg], list) or isinstance(args[arg], dict)) and p not in args[arg]:
                    continue
            except TypeError:
                continue
            if not os.path.isfile(get_persistent_files_dir() + p):
                print("FAIL: Persistent vars file '%s' does not exist!" % p)
                continue
            args[arg] = _replace_value(args[arg])
    return args


def _replace_keys(args, keys):
    """
    Some env variables are used for internal stuff, like 'name' or 'test'. This allows to replace them on the run.
    :param args: dict of values
    :param keys: dict of how to replace keys {original: new}
    :return: modifed args
    """
    for key in keys:
        if key in args:
            args[keys[key]] = args.pop(key)
    return args


def _apply_correct_type(values, keys):
    for value in values:
        try:
            values[value] = keys[value](values[value])
        except (KeyError, TypeError):
            pass
    return values


def get_env_args(args=None, persistent=None, replace_keys=None):
    """
    :param args: list of arguments
    :param persistent: list of possible persistent arguments
    :param replace_keys: dict of how to replace keys {original: new}
    :return: dict of env args
    """
    args = args or list()
    if not isinstance(args, dict):
        args = {arg: None for arg in args}
    persistent_vars = read_var(get_persistent_vars_file_name())
    persistent = persistent or persistent_vars if persistent_vars is not None else list()
    replace_keys = replace_keys or dict()
    arguments = {extra: None for extra in ["message", "expected_ret", "expected_out", "pkg", "command", "force"]
                 if extra not in args}
    arguments.update({a: None for a in args})
    for argument in arguments:
        try:
            arguments[argument] = read_env('fmf_' + argument)
        except KeyError:
            pass
    return _replace_keys(
        _apply_correct_type(
            remove_nones(
                _replace_env_args_with_persistent(
                    arguments,
                    persistent)),
            args),
        replace_keys)


def get_func_from_string(wrapper_object, command, local_functions=None):
    """
    :param wrapper_object: object that might contain method named in variable 'command'
    :param command: string with function to be found
    :param local_functions: dict of globals()
    :return: function pointer / None
    """
    local_functions = local_functions or dict()
    try:
        func = getattr(wrapper_object, command)
    except AttributeError:
        try:
            command = command.split(".")
            module = __import__(".".join(command[:-1]), globals(), locals(), level=0, fromlist=[command[-1]])
            func = getattr(module, command[-1])
        except KeyError:
            print("ERROR: Could not find function '%s' anywhere." % ".".join(command))
            return None
        except ValueError:
            # the function is is globals()
            func = local_functions[command[-1]]
    return func
