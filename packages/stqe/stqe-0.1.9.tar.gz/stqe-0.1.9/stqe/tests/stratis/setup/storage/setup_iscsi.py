#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from libsan.host.linux import hostname, is_service_running, install_package
from libsan.host.lio import TargetCLI
from libsan.host.iscsi import discovery_st, node_login
from stqe.host.atomic_run import atomic_run, parse_ret
from stqe.host.iscsi import auto_conf
from stqe.host.persistent_vars import write_var
from os import environ
from stqe.host.nfs_lock import setup_nfs_lock_iscsi


def setup_iscsi(test_type="stratis-general"):
    print("INFO: Setting up iSCSI with LUN %s." % test_type)
    errors = []

    install_package("iscsi-initiator-utils")

    if "brq" in hostname():
        auto_conf(test_type=test_type)

    else:
        wwn = f"iqn.1994-05.com.redhat:{test_type}"
        target = TargetCLI(path="/backstores/fileio")
        atomic_run("Creating fileio backstore",
                   command=target.create,
                   name="stratis-test",
                   file_or_dev="/var/tmp/stratis-test.img",
                   size="10G",
                   errors=errors,
                   )

        target.path = "/iscsi"
        atomic_run("Creating iscsi target",
                   wwn=wwn,
                   command=target.create,
                   errors=errors
                   )

        target.path = "/iscsi/" + wwn + "/" + "tpg1" + "/" + "luns"

        atomic_run("Creating lun with fileio backstore",
                   command=target.create,
                   storage_object="/backstores/fileio/stratis-test",
                   errors=errors,
                   )

        target.path = "/iscsi/" + wwn + "/" + "tpg1"

        atomic_run("Setting parameter generate_node_acls to '1'",
                   generate_node_acls=1,
                   group="attribute",
                   command=target.set,
                   errors=errors
                   )

        atomic_run("Setting parameter demo_mode_write_protect to '0'",
                   demo_mode_write_protect=0,
                   group="attribute",
                   command=target.set,
                   errors=errors
                   )

        atomic_run("Discovering local target",
                   target="127.0.0.1",
                   disc_db=True,
                   command=discovery_st,
                   errors=errors
                   )

        atomic_run("Trying to login to portal: 127.0.0.1",
                   portal="127.0.0.1",
                   command=node_login,
                   errors=errors
                   )

    # on RHEL 7 there is no LUN name in /dev/disk/by-path, just ID.
    _, local_disk = atomic_run(message="Getting iSCSI disk",
                               command=run,
                               return_output=True,
                               cmd="ls -la /dev/disk/by-path/ | grep '%s'" % test_type.replace("_", "-"),
                               errors=errors)
    if not local_disk:
        _, local_disk = atomic_run(message="Getting iSCSI disk through iscsiadm",
                                   command=run,
                                   return_output=True,
                                   cmd="iscsiadm -m session -P 3 | grep disk",
                                   errors=errors)
        if local_disk:
            # remove fail from 'ls -la ...'
            errors.pop()
        disk = local_disk.split()[3]
    else:
        disk = local_disk.split("../../").pop()

    if is_service_running("multipathd"):
        ret, multipath = atomic_run(message="Getting mpath device",
                                    command=run,
                                    return_output=True,
                                    cmd="multipath -l /dev/%s -v 1" % disk,
                                    errors=errors)

        atomic_run(message="Flushing mpath device %s" % multipath,
                   command=run,
                   cmd="multipath -f %s" % multipath,
                   errors=errors)

        atomic_run(message="Removing mpath device from disk %s" % disk,
                   command=run,
                   cmd="multipath -W /dev/%s" % disk,
                   errors=errors)

        atomic_run(message="Triggering udev",
                   command=run,
                   cmd="udevadm trigger; udevadm settle",
                   errors=errors)

    if "brq" in hostname():
        ret = atomic_run("NFS locking iscsi disk %s." % disk,
                         command=setup_nfs_lock_iscsi,
                         disk_name=disk,
                         errors=errors)
        if ret:
            print("FAIL: Could not get NFS lock for iscsi LUN.")
            return errors

    atomic_run("Cleaning superblock of device /dev/%s" % disk,
               command=run,
               cmd="dd if=/dev/zero of=/dev/%s bs=1M count=10" % disk,
               errors=errors)

    atomic_run("Writing var STRATIS_DEVICE",
               command=write_var,
               var={'STRATIS_DEVICE': "/dev/%s" % disk},
               errors=errors)

    atomic_run("Listing block devices.",
               command=run,
               cmd="lsblk",
               errors=errors)

    return errors


if __name__ == "__main__":
    lun_name = "stratis-general"
    try:
        lun_name = environ['fmf_lun_name']
    except KeyError:
        pass
    errs = setup_iscsi(lun_name)
    exit(parse_ret(errs))
