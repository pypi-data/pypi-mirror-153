#!/usr/bin/python

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import stqe.host.tc
from libsan.host.linux import install_package
from libsan.host.loopdev import create_loopdev, delete_loopdev
from libsan.host.lvm import vg_create, vg_remove, lv_create, lv_convert, lv_activate
from libsan.host.dmpd import cache_check, cache_dump, cache_restore, cache_repair, get_help, get_version
from libsan.host.cmdline import run
from stqe.host.atomic_run import atomic_run
from six.moves import range

TC = None


def init(args):
    print("INFO: Initializing test case")
    errors = []

    atomic_run("Creating loopdev 1 - 'fast' device",
               name=args["loop1"],
               size=args["loop1_size"],
               command=create_loopdev,
               errors=errors)

    atomic_run("Creating loopdev 2 - 'slow' device",
               name=args["loop2"],
               size=args["loop2_size"],
               command=create_loopdev,
               errors=errors)

    atomic_run("Creating VG",
               vg_name=args["group"],
               pv_name="/dev/" + args["loop1"] +
                       " /dev/" + args["loop2"],
               command=vg_create,
               errors=errors)

    atomic_run("Creating cache metadata volume",
               vg_name=args["group"] + " /dev/" + args["loop1"],
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
               vg_name=args["group"] + " /dev/" + args["loop1"],
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

    atomic_run("Creating filesystem on cache logical volume",
               cmd="mkfs.ext4 /dev/%s/%s" % (args["group"], args["origin"]),
               command=run,
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


def clean(args):
    print("INFO: Cleaning up")
    errors = []

    atomic_run("Removing VG",
               vg_name=args["group"],
               force=True,
               command=vg_remove,
               errors=errors)

    atomic_run("Deleting loopdev loop1",
               name=args["loop1"],
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


def runtime_test(args):
    print("\n#######################################\n")
    print("INFO: Testing cache tools runtime provided by device_mapper_persistent_data, iteration No. %s" %
           args["iteration"])

    errors = []

    atomic_run("Checking metadata",
               source_lv=args["swap"],
               source_vg=args["group"],
               command=cache_check,
               errors=errors)

    atomic_run("Checking metadata with clear-need-check-flag",
               source_lv=args["swap"],
               source_vg=args["group"],
               clear_needs_check_flag=True,
               command=cache_check,
               errors=errors)

    atomic_run("Checking metadata with super-block-only",
               source_lv=args["swap"],
               source_vg=args["group"],
               super_block_only=True,
               command=cache_check,
               errors=errors)

    atomic_run("Checking metadata with few paramethers",
               source_vg=args["group"],
               source_lv=args["swap"],
               skip_discards=True,
               skip_mappings=True,
               skip_hints=True,
               command=cache_check,
               errors=errors)

    atomic_run("Dumping metadata to standard output",
               source_vg=args["group"],
               source_lv=args["swap"],
               command=cache_dump,
               errors=errors)

    atomic_run("Calculating metadata size for cache of 64 blocks and 128 size",
               cmd="cache_metadata_size --block-size 64 --device-size 128",
               command=run,
               errors=errors)

    atomic_run("Calculating metadata size for cache of 128 nr blocks",
               cmd="cache_metadata_size --nr-blocks 128 --max-hint-width 4",
               command=run,
               errors=errors)

    atomic_run("Dumping metadata to file",
               source_vg=args["group"],
               source_lv=args["swap"],
               repair=True,
               output="/var/tmp/metadata",
               command=cache_dump,
               errors=errors)

    atomic_run("Checking metadata file",
               False,
               source_file="/var/tmp/metadata",
               command=cache_check,
               errors=errors)

    atomic_run("Restoring metadata with options",
               source_file="/var/tmp/metadata",
               target_vg=args["group"],
               target_lv=args["swap"],
               quiet=True,
               override_metadata_version=1,
               metadata_version=1,
               command=cache_restore,
               errors=errors)

    atomic_run("Restoring metadata from file",
               source_file="/var/tmp/metadata",
               target_vg=args["group"],
               target_lv=args["swap"],
               command=cache_restore,
               errors=errors)

    atomic_run("Repairing metadata to file",
               target_file="/var/tmp/metadata_repair",
               source_vg=args["group"],
               source_lv=args["swap"],
               command=cache_repair,
               errors=errors)

    atomic_run("Repairing metadata from file",
               source_file="/var/tmp/metadata_repair",
               target_vg=args["group"],
               target_lv=args["swap"],
               command=cache_repair,
               errors=errors)

    atomic_run("Simulating TTY for cache_restore",
               cmd="script --return -c 'cache_restore -i /var/tmp/metadata -o /dev/mapper/%s-%s' /dev/null" %
                   (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Checking metadata",
               source_vg=args["group"],
               source_lv=args["swap"],
               quiet=True,
               command=cache_check,
               errors=errors)

    print("\n#######################################\n")

    if len(errors) == 0:
        TC.tpass("Testing cache tools of device_mapper_persistent_data passed, iteration No. %s" % args["iteration"])
    else:
        TC.tfail("Testing cache tools of device_mapper_persistent_data failed with following errors: \n\t'" +
                 "\n\t ".join([str(i) for i in errors]) +
                 "\nIteration No. %s" % args["iteration"])
        return 1
    return 0


def errors_test(args):
    print("\n#######################################\n")
    print("INFO: Testing cache tools errors provided by device_mapper_persistent_data, iteration No. %s" %
           args["iteration"])

    errors = []

    functions = ["cache_check", "cache_dump", "cache_metadata_size", "cache_repair", "cache_restore"]

    # Sanity to check for missing input
    for func in functions:
        atomic_run("Validating missing input",
                   False,
                   cmd=func,
                   command=run,
                   errors=errors)

    # Sanity to check with wrong input
    for func in functions:
        atomic_run("Validating wrong input",
                   False,
                   cmd=func + " wrong",
                   command=run,
                   errors=errors)

    # Sanity to check with wrong option
    for func in functions:
        atomic_run("Validating wrong option",
                   False,
                   cmd=func + " -wrong",
                   command=run,
                   errors=errors)

    # Sanity to check with wrong -- option
    for func in functions:
        atomic_run("Validating wrong -- option",
                   False,
                   cmd=func + " --wrong",
                   command=run,
                   errors=errors)

    # Sanity to check present functions with -h
    for func in functions:
        atomic_run("Checking help of command",
                   cmd="%s" % func,
                   command=get_help,
                   errors=errors)

    # Sanity to check present functions with -V
    for func in functions:
        atomic_run("Checking version of command",
                   cmd="%s" % func,
                   command=get_version,
                   errors=errors)

    atomic_run("Checking metadata of non-metadata file",
               False,
               cmd="cache_check README",
               command=run,
               errors=errors)

    atomic_run("Checking metadata of non-existent file",
               False,
               cmd="cache_check WRONG",
               command=run,
               errors=errors)

    atomic_run("Checking metadata of non-regular file",
               False,
               cmd="cache_check /dev/mapper/control",
               command=run,
               errors=errors)

    atomic_run("Calculating metadata size for cache of 64 blocks",
               False,
               cmd="cache_metadata_size --block-size 64",
               command=run,
               errors=errors)

    atomic_run("Calculating metadata size for cache of 128 size",
               False,
               cmd="cache_metadata_size --device-size 128",
               command=run,
               errors=errors)

    atomic_run("Calculating metadata size for cache of 64 blocks and 128 size and 128 nr blocks",
               False,
               cmd="cache_metadata_size --block-size 64 --device-size 128 --nr-blocks 128",
               command=run,
               errors=errors)

    atomic_run("Repairing metadata without output",
               False,
               cmd="cache_repair -i /var/tmp/metadata_repair",
               command=run,
               errors=errors)

    atomic_run("Restoring metadata with wrong options",
               False,
               cmd="cache_restore -i /var/tmp/metadata -o /dev/mapper/%s-%s --wrong test" % (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Restoring metadata with wrong metadata version",
               False,
               source_file="/var/tmp/metadata",
               target_vg=args["group"],
               target_lv=args["swap"],
               metadata_version=12445,
               command=cache_restore,
               errors=errors)

    atomic_run("Restoring metadata with wrong source",
               False,
               cmd="cache_restore -i /var/tmp/wrong.wrong -o /dev/mapper/%s-%s" % (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Restoring metadata with bit source",
               False,
               source_file="/var/tmp/metadata_repair",
               target_vg=args["group"],
               target_lv=args["swap"],
               command=cache_restore,
               errors=errors)

    atomic_run("Restoring metadata without output",
               False,
               cmd="cache_restore -i /var/tmp/metadata",
               command=run,
               errors=errors)

    atomic_run("Restoring metadata with options",
               pkg=["device-mapper-persistent-data", "0.7.3-2"],
               source_file="/var/tmp/metadata",
               target_vg=args["group"],
               target_lv=args["swap"],
               omit_clean_shutdown=True,
               command=cache_restore,
               errors=errors)

    atomic_run("Checking metadata",
               source_vg=args["group"],
               source_lv=args["swap"],
               command=cache_check,
               errors=errors)

    # FIXME: Using BZ1255552 for this, find other way
    atomic_run("Corrupting mappings on metadata device",
               False,
               source_file="Makefile",
               target_vg=args["group"],
               target_lv=args["swap"],
               command=cache_restore,
               errors=errors)

    atomic_run("Checking corrupted mappings",
               False,
               source_vg=args["group"],
               source_lv=args["swap"],
               command=cache_check,
               errors=errors)

    atomic_run("Trying to fail while dumping metadata",
               False,
               source_vg=args['group'],
               source_lv=args['swap'],
               output="/var/tmp/metadata",
               command=cache_dump,
               errors=errors)

    atomic_run("Repairing metadata",
               source_vg=args['group'],
               source_lv=args['swap'],
               target_file="/var/tmp/metadata_repair",
               command=cache_repair,
               errors=errors)

    atomic_run("Corrupting metadata on device",
               cmd="echo 'nothing' >> /dev/mapper/%s-%s" % (args['group'], args['swap']),
               command=run,
               errors=errors)

    atomic_run("Trying to fail while repairing metadata",
               False,
               source_vg=args['group'],
               source_lv=args['swap'],
               target_file="/var/tmp/metadata_repair",
               command=cache_repair,
               errors=errors)

    atomic_run("Trying to fail while dumping metadata",
               False,
               source_vg=args['group'],
               source_lv=args['swap'],
               output="/var/tmp/metadata",
               command=cache_dump,
               errors=errors)

    atomic_run("Checking corrupted metadata",
               False,
               source_vg=args["group"],
               source_lv=args["swap"],
               command=cache_check,
               errors=errors)

    print("\n#######################################\n")

    if len(errors) == 0:
        TC.tpass("Testing cache tools errors of device_mapper_persistent_data passed, iteration No. %s" %
                 args["iteration"])
    else:
        TC.tfail("Testing cache tools errors of device_mapper_persistent_data failed with following errors: \n\t'" +
                 "\n\t ".join([str(i) for i in errors]) +
                 "\nIteration No. %s" % args["iteration"])
        return 1
    return 0


def main():
    # Initialize Test Case
    global TC
    TC = stqe.host.tc.TestClass()

    args = {"loop1": "loop1",
            "loop1_size": 2048,
            "loop2": "loop2",
            "loop2_size": 4128,
            "group": "vgtest",
            "origin": "origin",
            "data": "cache_data",
            "meta": "cache_meta",
            "pool": "cache_pool",
            "swap": "swapvol"
            }

    # Initialization
    packages = ["device-mapper-persistent-data"]
    install_packages(packages)

    init(args)

    # run it 3 times
    for i in range(1):
        args["iteration"] = i
        runtime_test(args)
        errors_test(args)

    clean(args)

    if not TC.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: Test pass")
    sys.exit(0)


if __name__ == "__main__":
    main()
