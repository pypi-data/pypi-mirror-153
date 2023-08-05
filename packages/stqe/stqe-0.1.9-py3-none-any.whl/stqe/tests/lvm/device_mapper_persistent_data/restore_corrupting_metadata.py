#!/usr/bin/python

#
# Related BZ:
#       1255552
#

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import stqe.host.tc
from stqe.host.atomic_run import atomic_run
from libsan.host.cmdline import run
from libsan.host.dmpd import thin_restore, thin_dump, thin_check, cache_dump, cache_check, cache_restore
from libsan.host.linux import install_package
from libsan.host.loopdev import create_loopdev, delete_loopdev
from libsan.host.lvm import vg_create, vg_remove, lv_create, lv_activate, lv_deactivate, lv_convert

TC = None


def _mount_thin_lv(vg_name, lv_name):
    run("mkdir -p /mnt/%s" % lv_name, verbose=True)
    run("mkfs.ext4 /dev/%s/%s" % (vg_name, lv_name), verbose=True)
    run("mount /dev/%s/%s /mnt/%s/" % (vg_name, lv_name, lv_name), verbose=True)


def _unmount_thin_lv(lv_name):
    run("umount -f /mnt/%s/" % lv_name, verbose=True)
    run("rm -rf /mnt/%s" % lv_name, verbose=True)


def create_lvs(args, iteration, errors):
    if iteration == 1:
        atomic_run("Creating thin LV.",
                   vg_name=args["group"] + "/" + args["pool"],
                   lv_name=args["vol"],
                   options=["-T", "-V 10"],
                   command=lv_create,
                   errors=errors)

        atomic_run("Deactivating thin LV.",
                   lv_name=args["vol"],
                   vg_name=args["group"],
                   command=lv_deactivate,
                   errors=errors)

    elif iteration == 2:
        atomic_run("Creating thin LV.",
                   vg_name=args["group"] + "/" + args["pool"],
                   lv_name=args["vol"],
                   options=["-T", "-V 10"],
                   command=lv_create,
                   errors=errors)

        atomic_run("Creating filesystem on LV.",
                   cmd="mkfs.ext4 /dev/%s/%s" % (args['group'], args['vol']),
                   command=run,
                   errors=errors)

        atomic_run("Deactivating thin LV.",
                   lv_name=args["vol"],
                   vg_name=args["group"],
                   command=lv_deactivate,
                   errors=errors)

    elif iteration == 3:
        for i in range(2):
            atomic_run("Creating thin LV No. %s." % i,
                       vg_name=args["group"] + "/" + args["pool"],
                       lv_name=args["vol"] + str(i),
                       options=["-T", "-V 10"],
                       command=lv_create,
                       errors=errors)

            atomic_run("Deactivating thin LV No. %s." % i,
                       lv_name=args["vol"] + str(i),
                       vg_name=args["group"],
                       command=lv_deactivate,
                       errors=errors)

    elif iteration == 4:
        for i in range(2):
            atomic_run("Creating thin LV No. %s." % i,
                       vg_name=args["group"] + "/" + args["pool"],
                       lv_name=args["vol"] + str(i),
                       options=["-T", "-V 10"],
                       command=lv_create,
                       errors=errors)
            if i == 1:
                atomic_run("Creating filesystem on LV No. %s." % i,
                           cmd="mkfs.ext4 /dev/%s/%s" % (args['group'], args['vol'] + str(i)),
                           command=run,
                           errors=errors)

            atomic_run("Deactivating thin LV No. %s." % i,
                       lv_name=args["vol"] + str(i),
                       vg_name=args["group"],
                       command=lv_deactivate,
                       errors=errors)

    elif iteration == 5:
        for i in range(2):
            atomic_run("Creating thin LV No. %s." % i,
                       vg_name=args["group"] + "/" + args["pool"],
                       lv_name=args["vol"] + str(i),
                       options=["-T", "-V 10"],
                       command=lv_create,
                       errors=errors)
            if i == 2:
                atomic_run("Creating filesystem on LV No. %s." % i,
                           cmd="mkfs.ext4 /dev/%s/%s" % (args['group'], args['vol'] + str(i)),
                           command=run,
                           errors=errors)

            atomic_run("Deactivating thin LV No. %s." % i,
                       lv_name=args["vol"] + str(i),
                       vg_name=args["group"],
                       command=lv_deactivate,
                       errors=errors)

    elif iteration == 6:
        for i in range(2):
            atomic_run("Creating thin LV No. %s." % i,
                       vg_name=args["group"] + "/" + args["pool"],
                       lv_name=args["vol"] + str(i),
                       options=["-T", "-V 10"],
                       command=lv_create,
                       errors=errors)

            atomic_run("Creating filesystem on LV No. %s." % i,
                       cmd="mkfs.ext4 /dev/%s/%s" % (args['group'], args['vol'] + str(i)),
                       command=run,
                       errors=errors)

            atomic_run("Deactivating thin LV No. %s." % i,
                       lv_name=args["vol"] + str(i),
                       vg_name=args["group"],
                       command=lv_deactivate,
                       errors=errors)


def thin_init(args, iteration):
    print("INFO: Initializing test case, iteration No. %s" % iteration)
    errors = []

    atomic_run("Creating loopdev",
               name=args["loop"],
               size=args["loop_size"],
               command=create_loopdev,
               errors=errors)

    atomic_run("Creating VG",
               vg_name=args["group"],
               pv_name="/dev/" + args["loop"],
               command=vg_create,
               errors=errors)

    atomic_run("Creating thin pool",
               vg_name=args["group"],
               lv_name=args["pool"],
               options=["-T", "-L 100"],
               command=lv_create,
               errors=errors)

    # Create LVs each time a bit different to cover all the conditions
    create_lvs(args, iteration, errors)

    atomic_run("Deactivating pool",
               lv_name=args["pool"],
               vg_name=args["group"],
               command=lv_deactivate,
               errors=errors)

    atomic_run("Creating swap LV",
               vg_name=args["group"],
               lv_name=args["swap"],
               options=["-L 100"],
               command=lv_create,
               errors=errors)

    atomic_run("Deactivating swap",
               lv_name=args["swap"],
               vg_name=args["group"],
               command=lv_deactivate,
               errors=errors)

    atomic_run("Swapping metadata",
               vg_name=args["group"],
               lv_name=args["swap"],
               options=["-y", "--thinpool " + args["group"] + "/" + args["pool"],
                        "--poolmetadata "],
               command=lv_convert,
               errors=errors)

    atomic_run("Activating swap",
               lv_name=args["swap"],
               vg_name=args["group"],
               command=lv_activate,
               errors=errors)

    if len(errors) == 0:
        TC.tpass("Initialization No. %s passed" % iteration)
    else:
        TC.tfail("Initialization No. %s failed with following errors: \n\t'" % iteration +
                 "\n\t ".join([str(i) for i in errors]))
        return 1
    return 0


def cache_init(args):
    print("INFO: Initializing test case.")
    errors = []

    atomic_run("Creating loopdev 1 - 'fast' device",
               name=args["loop"],
               size=args["loop_size"],
               command=create_loopdev,
               errors=errors)

    atomic_run("Creating loopdev 2 - 'slow' device",
               name=args["loop2"],
               size=args["loop2_size"],
               command=create_loopdev,
               errors=errors)

    atomic_run("Creating VG",
               vg_name=args["group"],
               pv_name="/dev/" + args["loop"] +
                       " /dev/" + args["loop2"],
               command=vg_create,
               errors=errors)

    atomic_run("Creating cache metadata volume",
               vg_name=args["group"] + " /dev/" + args["loop"],
               lv_name=args["meta"],
               options=["-L 12"],
               command=lv_create,
               errors=errors)

    atomic_run("Creating origin volume",
               vg_name=args["group"] + " /dev/" + args["loop2"],
               lv_name=args["origin"],
               options=["-L 2G"],
               command=lv_create,
               errors=errors)

    atomic_run("Creating cache data volume",
               vg_name=args["group"] + " /dev/" + args["loop"],
               lv_name=args["data"],
               options=["-L 1G"],
               command=lv_create,
               errors=errors)

    atomic_run("Creating cache pool",
               vg_name=args["group"],
               lv_name=args["data"],
               options=["-y --type cache-pool", "--cachemode writeback", "--poolmetadata %s/%s" %
                        (args["group"], args["meta"])],
               command=lv_convert,
               errors=errors)

    atomic_run("Creating cache logical volume",
               vg_name=args["group"],
               lv_name=args["origin"],
               options=["-y", "--type cache", "--cachepool %s/%s" %
                        (args["group"], args["data"])],
               command=lv_convert,
               errors=errors)

    atomic_run("Splitting cache logical volume",
               vg_name=args["group"],
               lv_name=args["origin"],
               options=["-y", "--splitcache"],
               command=lv_convert,
               errors=errors)

    atomic_run("Creating swap LV",
               vg_name=args["group"],
               lv_name=args["swap"],
               options=["-L 100"],
               command=lv_create,
               errors=errors)

    atomic_run("Swapping metadata",
               vg_name=args["group"],
               lv_name=args["swap"],
               options=["-y", "--cachepool " + args["group"] + "/" + args["data"],
                        "--poolmetadata "],
               command=lv_convert,
               errors=errors)

    atomic_run("Activating swap",
               lv_name=args["swap"],
               vg_name=args["group"],
               command=lv_activate,
               errors=errors)

    if len(errors) == 0:
        TC.tpass("Initialization passed")
    else:
        TC.tfail("Initialization failed with following errors: \n\t'" +
                 "\n\t ".join([str(i) for i in errors]))
        return 1
    return 0


def thin_clean(args):
    print("INFO: Cleaning up")
    errors = []

    # restoring metadata device after corrupting it
    atomic_run("Repairing metadata device",
               source_file="/var/tmp/metadata",
               target_vg=args["group"],
               target_lv=args["swap"],
               quiet=True,
               command=thin_restore,
               errors=errors)

    # thinpool got activated after checking its metadata to get bad checksum
    atomic_run("Deactivating pool",
               lv_name=args["pool"],
               vg_name=args["group"],
               command=lv_deactivate,
               errors=errors)

    atomic_run("Deactivating swap",
               lv_name=args["swap"],
               vg_name=args["group"],
               command=lv_deactivate,
               errors=errors)

    atomic_run("Swapping back metadata",
               vg_name=args["group"],
               lv_name=args["swap"],
               options=["-y", "--thinpool " + args["group"] + "/" + args["pool"],
                        "--poolmetadata "],
               command=lv_convert,
               errors=errors)

    atomic_run("Removing VG",
               vg_name=args["group"],
               force=True,
               command=vg_remove,
               errors=errors)

    atomic_run("Deleting loopdev",
               name=args["loop"],
               command=delete_loopdev,
               errors=errors)

    atomic_run("Deleting metadata file",
               cmd="rm -f /var/tmp/metadata",
               command=run,
               errors=errors)

    if len(errors) == 0:
        TC.tpass("Cleanup passed")
    else:
        TC.tfail("Cleanup failed with following errors: \n\t'" +
                 "\n\t ".join([str(i) for i in errors]))
        print(errors)
        return 1
    return 0


def cache_clean(args):
    print("INFO: Cleaning up")
    errors = []

    atomic_run("Removing VG",
               vg_name=args["group"],
               force=True,
               command=vg_remove,
               errors=errors)

    atomic_run("Deleting loopdev loop1",
               name=args["loop"],
               command=delete_loopdev,
               errors=errors)

    atomic_run("Deleting loopdev loop2",
               name=args["loop2"],
               command=delete_loopdev,
               errors=errors)

    atomic_run("Deleting metadata file",
               cmd="rm -f /var/tmp/metadata",
               command=run,
               errors=errors)

    atomic_run("Deleting repair metadata file",
               cmd="rm -f /var/tmp/metadata_repair",
               command=run,
               errors=errors)

    if len(errors) == 0:
        TC.tpass("Cleanup passed")
    else:
        TC.tfail("Cleanup failed with following errors: \n\t'" +
                 "\n\t ".join([str(i) for i in errors]))
        print(errors)
        return 1
    return 0


def install_packages(packages):
    for package in packages:
        install_package(package)


def thin(args, iteration):
    print("\n#######################################\n")
    print("INFO: Testing restoring corruption with thin_restore, iteration No. %s" % iteration)

    errors = []

    atomic_run("Dumping metadata to file",
               formatting="xml",
               source_vg=args["group"],
               source_lv=args["swap"],
               output="/var/tmp/metadata",
               command=thin_dump,
               errors=errors)

    atomic_run("Checking metadata",
               source_vg=args["group"],
               source_lv=args["swap"],
               command=thin_check,
               errors=errors)

    atomic_run("Restoring metadata from nonexistent file",
               False,
               cmd="thin_restore -i /var/tmp/wrong.wrong -o /dev/mapper/%s-%s" % (args['group'], args['swap']),
               command=run,
               errors=errors)

    # should pass without error on the last iteration
    if iteration != 6:
        atomic_run("Checking metadata",
                   pkg=["device-mapper-persistent-data", "0.7.3", "1.el7"],
                   source_vg=args["group"],
                   source_lv=args["swap"],
                   command=thin_check,
                   errors=errors)
    else:
        atomic_run("Checking metadata",
                   source_vg=args["group"],
                   source_lv=args["swap"],
                   command=thin_check,
                   errors=errors)

    print("\n#######################################\n")

    if len(errors) == 0:
        TC.tpass("Testing restoring corruption with thin_restore passed, iteration No. %s" % iteration)
    else:
        TC.tfail("Testing restoring corruption with thin_restore failed with following errors: \n\t'" +
                 "\n\t ".join([str(i) for i in errors]) +
                 "\nIteration No. %s" % iteration)
        return 1
    return 0


def cache(args):
    print("\n#######################################\n")
    print(
        "INFO: Testing restoring corruption with cache_restore.")

    errors = []

    atomic_run("Dumping metadata to file",
               source_vg=args["group"],
               source_lv=args["swap"],
               output="/var/tmp/metadata",
               command=cache_dump,
               errors=errors)

    atomic_run("Checking metadata",
               source_vg=args["group"],
               source_lv=args["swap"],
               command=cache_check,
               errors=errors)

    atomic_run("Restoring metadata with options",
               False,
               source_file="/var/tmp/metadata",
               target_vg=args["group"],
               target_lv=args["swap"],
               omit_clean_shutdown=True,
               command=cache_restore,
               errors=errors)

    atomic_run("Restoring metadata from nonexistent file",
               False,
               cmd="cache_restore -i /var/tmp/wrong.wrong -o /dev/mapper/%s-%s" % (args['group'], args['swap']),
               command=run,
               errors=errors)

    # The fail here is caused by using "omit-clean-shotdown" before
    atomic_run("Checking metadata",
               pkg=["device-mapper-persistent-data", "0.7.3", "1.el7"],
               source_vg=args["group"],
               source_lv=args["swap"],
               command=cache_check,
               errors=errors)

    print("\n#######################################\n")

    if len(errors) == 0:
        TC.tpass("Testing restoring corruption with thin_restore passed")
    else:
        TC.tfail("Testing restoring corruption with thin_restore failed with following errors: \n\t'" +
                 "\n\t ".join([str(i) for i in errors]))
        return 1
    return 0


def main():
    # Initialize Test Case
    global TC
    TC = stqe.host.tc.TestClass()

    args = {"loop": "loop1",
            "loop_size": 2048,
            "loop2": "loop2",
            "loop2_size": 4128,
            "group": "vgtest",
            "pool": "thinpool",
            "vol": "thinvol",
            "number of vols": 10,
            "origin": "origin",
            "data": "cache_data",
            "meta": "cache_meta",
            "swap": "swapvol"}

    # Initialization
    packages = ["device-mapper-persistent-data"]
    install_packages(packages)

    # thin_restore testing
    for i in range(1, 7):
        thin_init(args, i)
        thin(args, i)
        thin_clean(args)

    # cache_restore testing
    cache_init(args)
    cache(args)
    cache_clean(args)

    if not TC.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: Test pass")
    sys.exit(0)


if __name__ == "__main__":
    main()
