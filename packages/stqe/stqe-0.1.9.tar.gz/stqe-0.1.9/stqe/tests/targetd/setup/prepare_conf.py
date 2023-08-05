#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import os
from stqe.host.atomic_run import parse_ret

targetd_cfg = "/etc/target/targetd.yaml"


def prepare_conf():
    errors = []
    do_nothing = True

    if not os.path.isfile(targetd_cfg):
        print("FAIL: %s does not exist" % targetd_cfg)
        errors.append("FAIL: %s does not exist" % targetd_cfg)
        return errors

    with open(targetd_cfg, "r") as read_config:
        lines = read_config.readlines()
    if lines[0].startswith("# modified"):
        return True
    for line in lines:
        if line.startswith("# defaults below"):
            do_nothing = False
            continue
        if do_nothing or line.startswith("# log level"):
            continue
        if line.startswith("# "):
            lines[lines.index(line)] = line.lstrip("# ")
            continue
        lines[lines.index(line)] = line.lstrip("#")
    lines.insert(0, "# Modified by prepare_conf.py\n")
    with open(targetd_cfg, "w") as write_config:
        write_config.writelines(lines)

    return errors


if __name__ == "__main__":
    errs = prepare_conf()
    exit(parse_ret(errs))
