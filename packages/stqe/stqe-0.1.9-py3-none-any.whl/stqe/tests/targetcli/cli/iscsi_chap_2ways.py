#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import libsan.host.iscsi as iscsi
from os import environ
from libsan.host.lio import TargetCLI
from stqe.host.persistent_vars import read_var
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.iscsi import discovery_st, node_login, clean_up


def clean_target_chap_settigs():
    """
    Disabling CHAP on a target by removing CHAP parameters from groups auth and discovery_auth.
    :return:
    List of errors.
    """
    errors = []

    target = TargetCLI()
    tpg = read_var("TPG")
    target_iqn = read_var("TARGET_IQN")

    args = [{"userid": ''}, {"password": ''}, {"mutual_userid": ''}, {"mutual_password": ''}]
    groups = ["auth", "discovery_auth"]

    for group in groups:
        if group == "auth":
            target.path = "/iscsi/" + target_iqn + "/" + tpg
        elif group == "discovery_auth":
            target.path = "/iscsi"
        for arg in args:
            atomic_run("Setting parameter: %s to '' in group %s" % (list(arg.keys())[0], group),
                       group=group,
                       command=target.set,
                       errors=errors,
                       **arg
                       )

    return errors


def iscsi_chap_pass():
    errors = []
    ip_address = environ["fmf_target_ip"]
    expected_ret = environ["fmf_expected_ret"]
    target_iqn = read_var("TARGET_IQN")
    username = read_var("CHAP_USERID")
    password = read_var("CHAP_PASSWORD")
    mutual_userid = read_var("CHAP_MUTUAL_USERID")
    mutual_password = read_var("CHAP_MUTUAL_PASSWORD")

    atomic_run("Setting auth parameters in iscsid config",
               target_user=username,
               target_pass=password,
               initiator_user=mutual_userid,
               initiator_pass=mutual_password,
               command=iscsi.set_chap,
               errors=errors
               )

    atomic_run("Discovering local target",
               target=ip_address,
               disc_db=True,
               command=discovery_st,
               errors=errors
               )

    atomic_run("Trying to login to target: %s" % ip_address,
               expected_ret=expected_ret,
               target=target_iqn,
               command=node_login,
               errors=errors
               )

    atomic_run("Cleaning up",
               command=clean_up,
               errors=errors
               )

    atomic_run("Disabling CHAP",
               command=iscsi.disable_chap,
               errors=errors
               )

    return errors


if __name__ == "__main__":
    errs = iscsi_chap_pass()
    errs += clean_target_chap_settigs()
    exit(parse_ret(errs))
