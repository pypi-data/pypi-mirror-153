#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var
from libsan.host.lio import TargetCLI

sub_table = {"0": "1", "1": "0"}
unsupported = ["alua_support", "block_size", "emulate_rest_reord", "emulate_dpo", "emulate_fua_read", "pi_prot_verify",
               "emulate_tpws", "unmap_zeroes_data", "pi_prot_format", "pgr_support"]


def compare_attributes(dict1, dict2):
    errors = []

    for attribute in dict1:
        if int(dict1[attribute]) != int(dict2[attribute]):
            print("FAIL: " + attribute + " " + str(dict1[attribute]) +
                          " != " + dict2[attribute])
            errors.append("FAIL: " + attribute + " " + str(dict1[attribute]) +
                          " != " + dict2[attribute])

    return errors


def fileio_attributes_test():
    default_attr = dict()
    changed_attr = dict()

    errors = []

    name = read_var("FILEIO_NAME")
    target = TargetCLI(path="/backstores/fileio/%s" % name)

    ret, data = atomic_run("Getting parameters from group attribute",
                           group="attribute",
                           command=target.get,
                           return_output=True,
                           errors=errors
                           )
    if ret != 0:
        print("FAIL: Can not get attributes for %s" % name)
        errors.append("FAIL: Can not get attributes for %s" % name)
        return errors

    attributes = data.splitlines()
    end = len(attributes)

    for attribute in attributes:
        if attributes.index(attribute) < end - 1 and "[ro]" not in attribute and \
                attributes[attributes.index(attribute) + 1].startswith("---"):
            attr = attribute.split("=")
            if attr[0] in unsupported:
                continue
            default_attr[attr[0]] = attr[1]

    for attribute in default_attr.keys():
        if int(default_attr[attribute]) == 0 or int(default_attr[attribute]) == 1:
            default_attr[attribute] = sub_table[default_attr[attribute]]
        else:
            default_attr[attribute] = int(int(default_attr[attribute]) / 2)

    atomic_run("Changing parameters in group attribute",
               group="attribute",
               command=target.set,
               errors=errors,
               **default_attr
               )

    ret, data = atomic_run("Getting parameters from group attribute",
                           group="attribute",
                           command=target.get,
                           return_output=True,
                           errors=errors,
                           **default_attr
                           )

    if ret != 0:
        print("FAIL: Cannot get attributes for %s" % name)
        errors.append("FAIL: Cannot get attributes for %s" % name)
        return errors

    attr_list = data.splitlines()

    for i in attr_list:
        attr = i.split("=")
        changed_attr[attr[0]] = attr[1]

    errors += compare_attributes(default_attr, changed_attr)

    return errors


if __name__ == "__main__":
    errs = fileio_attributes_test()
    exit(parse_ret(errs))
