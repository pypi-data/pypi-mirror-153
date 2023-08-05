#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.persistent_vars import read_var
from libsan.host.qemu_img import delete_image


def delete_qcow():
    errors = []

    name = read_var("IMAGE_NAME")
    path = read_var("IMAGE_PATH")

    atomic_run("Deleting qcow image %s" % name,
               name=name,
               image_path=path,
               command=delete_image,
               errors=errors
               )

    return errors


if __name__ == "__main__":
    errs = delete_qcow()
    exit(parse_ret(errs))
