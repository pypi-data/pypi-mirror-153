#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.linux import compare_version
from time import localtime, strftime
import os
import json


class Variables:
    # global variables persistent across libraries and instances
    def __init__(self):
        pass

    logging_level = 20
    tests_to_run = "*"
    tier_to_test = 3
    no_run = False
    bz = []  # list of BZ numbers


class Logger:
    def __init__(self):
        pass

    def debug(self, message):
        if Variables.logging_level < 20:
            if message.startswith("\n"):
                print("\nDEBUG: [%s] " % self.get_time() + message[1:])
            else:
                print("DEBUG: [%s] " % self.get_time() + message)

    def info(self, message):
        if message.startswith("\n"):
            print("\nINFO: [%s] " % self.get_time() + message[1:])
        else:
            print("INFO: [%s] " % self.get_time() + message)

    def warn(self, message):
        if message.startswith("\n"):
            print("\nWARN: [%s] " % self.get_time() + message[1:])
        else:
            print("WARN: [%s] " % self.get_time() + message)

    def fail(self, message):
        if message.startswith("\n"):
            print("\nFAIL: [%s] " % self.get_time() + message[1:])
        else:
            print("FAIL: [%s] " % self.get_time() + message)

    @staticmethod
    def get_time():
        return strftime("%Y-%m-%d %H:%M:%S", localtime())


def atomic_run(message, success=True, return_output=False, expected_ret=None, expected_out=None, **kwargs):
    def log_error(error_message, errors_list):
        logger.fail(error_message)
        if isinstance(errors_list, list):
            errors_list.append(error_message)
        else:
            logger.fail("atomic_run got 'errors' value that is not list.")

    def is_expected_out_in_out(out, exp_out):
        out = out.replace("\'", "").replace("\"", "")
        if isinstance(exp_out, list):
            # check all from list are in output
            if all([True if e in out else False for e in exp_out]):
                return True
            else:
                return False
        if str(exp_out) in out:
            return True
        return False

    errors = kwargs.pop("errors")
    command = kwargs.pop("command")

    logger = Logger()

    # used to invert expected output before version of this package, list of ['package', 'version', (optional)'release']
    if 'pkg' in kwargs:
        pkg = [str(x) for x in kwargs.pop('pkg')]
        if len(pkg) == 2:
            pkg.append("")
        comparision = compare_version(*pkg)
        if isinstance(comparision, bool) and not comparision:
            logger.info("Expecting inverse output.")
            if expected_ret is None:
                success = not success
            elif expected_ret != 0:
                expected_ret = 0

    # This is dictionary to switch output to bash logic (0 == success) as in Python True == 1 and not 0
    switcher = {
        True: 0,
        False: 1
    }

    # switch bool to int using switcher to be consistent
    if isinstance(expected_ret, bool):
        try:
            expected_ret = switcher[expected_ret]
        except KeyError:
            pass
    if isinstance(success, bool):
        success = switcher[success]

    # match expected_ret to success in case we do not specify it
    if expected_ret is None:
        expected_ret = success

    params = []
    for a in kwargs:
        params.append(str(a) + " = " + str(kwargs[a]))
    if len(params) != 0:
        params = ", ".join([str(i) for i in params])
        message += " with params %s" % params
    logger.info("\n" + message)

    try:
        ret, output = command(return_output=True, **kwargs)
    except TypeError as e:
        if "takes no keyword arguments" in str(e):
            # this function takes no keyword arguments
            # let's assume there is only 1 kwarg for now
            ret = command(*[kwargs[arg] for arg in kwargs])
            output = ""
        else:
            # unexpected keyword argument return_output, let's try without it
            # and everything else...
            ret = command(**kwargs)
            output = ""
    # '1' gets implemented by python as 'True' and vice versa, switch it back
    if isinstance(ret, bool):
        ret = switcher[ret]

    should = {0: "succeed", 1: "fail"}
    logger.debug("Should %s" % should[success] + " with '%s'. " % expected_ret + "Got '%s'." % ret)
    if (success and ret != expected_ret and type(ret) == type(expected_ret)) or (
                    not success and ret != expected_ret and type(ret) == type(expected_ret)):
        if Variables.logging_level >= 20:
            logger.info("Should %s" % should[success] + " with '%s'. " % expected_ret + "Got '%s'." % ret)
        failed = "failed."
        if success == 1:
            failed = "did not fail."
        error = message + " with params %s %s" % (params, failed)
        log_error(error, errors)

    if expected_out and not is_expected_out_in_out(output, expected_out):
        log_error("Could not find '%s' in returned output, got '%s'." % (expected_out, output), errors)

    if return_output:
        return ret, output
    else:
        return ret


def parse_ret(errors):
    if errors == list():
        return 0
    else:
        # write errors to file for parsing at the end
        try:
            test_name = os.environ['fmf_name']
        except KeyError:
            print("FAIL: Could not get test name though os.environ. Not running error parsing.")
            return 1

        path = '/tmp/test_errors.json'
        if os.path.isfile(path):
            with open(path, 'r') as f:
                dict = json.load(f)
        else:
            dict = {}

        dict[test_name] = errors
        with open(path, 'w') as f:
            json.dump(dict, f)
        return 1
