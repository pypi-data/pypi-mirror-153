#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.persistent_vars import read_var, write_var
from stqe.host.atomic_run import atomic_run, parse_ret
from libsan.host.lio import TargetCLI
from random import randint
import string
import secrets
from os import environ


def remove_nones(kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


def rand_string(length):
    """
    Creates random string of length passed as parameter.
    :param length: integer representing length of the string
    :return:
    None: if length is not integer
    string: with random characters
    """

    if not isinstance(length, int):
        return None

    alphabet = string.ascii_letters + string.digits + '.-+@_=:/[],~'  # rfc7143#section-6.1
    # Allowed in targetcli:
    # https://github.com/open-iscsi/configshell-fb/blob/b4923ee5591d8b980003150e0ba6ffe512d8c9da/configshell/shell.py#L116
    generated_string = ''.join(secrets.choice(alphabet) for _ in range(length))

    return str(generated_string)


def configure_chap():
    errors = []
    target_iqn = read_var("TARGET_IQN")
    tpg = read_var("TPG")
    # supported fmf arguments
    args = {"random": False, "userid": None, "password": None,
            "mutual_userid": None, "mutual_password": None, "chap_ways": 1}
    # Getting arguments from fmf
    for arg in args.keys():
        try:
            if arg == "chap_ways":
                args[arg] = int(environ["fmf_%s" % arg])
                continue
            args[arg] = environ["fmf_%s" % arg]
        except KeyError:
            pass

    if args["random"]:  # if random is true, generate userid and password randomly
        if args["chap_ways"] == 2:
            args["mutual_userid"] = rand_string(randint(1, 255))
            args["mutual_password"] = rand_string(randint(1, 255))
        args["userid"] = rand_string(randint(1, 255))
        args["password"] = rand_string(randint(1, 255))
    for i in ["random", "chap_ways"]:  # removing these args from dict because this dict is used as kwargs in atomic run
        args.__delitem__(i)

    target = TargetCLI()

    target.path = "/iscsi"

    atomic_run("Enabling discovery_auth and setting userid and password",
               enable=1,
               group="discovery_auth",
               command=target.set,
               errors=errors,
               **remove_nones(args)
               )

    target.path = "/iscsi/" + target_iqn + "/" + tpg

    atomic_run("Enabling authentication and generate node acls",
               group="attribute",
               authentication=1,
               generate_node_acls=1,
               command=target.set,
               errors=errors
               )

    atomic_run("Setting userid and password in auth group",
               group="auth",
               command=target.set,
               errors=errors,
               **remove_nones(args)
               )

    if args["mutual_userid"] is not None and args["mutual_password"] is not None:
        atomic_run("Writing var CHAP_MUTUAL_USERID",
                   command=write_var,
                   var={"CHAP_MUTUAL_USERID": args["mutual_userid"]},
                   errors=errors)

        atomic_run("Writing var CHAP_MUTUAL_PASSWORD",
                   command=write_var,
                   var={"CHAP_MUTUAL_PASSWORD": args["mutual_password"]},
                   errors=errors)

    atomic_run("Writing var CHAP_USERID",
               command=write_var,
               var={"CHAP_USERID": args["userid"]},
               errors=errors)

    atomic_run("Writing var CHAP_PASSWORD",
               command=write_var,
               var={"CHAP_PASSWORD": args["password"]},
               errors=errors)

    return errors


if __name__ == "__main__":
    errs = configure_chap()
    exit(parse_ret(errs))
