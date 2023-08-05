#!/usr/bin/python

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import stqe.host.tc
from stqe.host.atomic_run import atomic_run
from libsan.host.cmdline import run
from libsan.host.dmpd import thin_restore, thin_check, thin_ls, thin_dump, thin_rmap, thin_delta, thin_repair, \
    thin_trim, get_help, get_version
from libsan.host.linux import install_package
from libsan.host.loopdev import create_loopdev, delete_loopdev
from libsan.host.lvm import vg_create, vg_remove, lv_create, lv_remove, lv_activate, lv_deactivate, lv_convert

TC = None


def _mount_thin_lv(vg_name, lv_name):
    ret = run("mkdir -p /mnt/%s" % lv_name, verbose=True)
    ret += run("mkfs.ext4 /dev/%s/%s" % (vg_name, lv_name), verbose=True)
    ret += run("mount /dev/%s/%s /mnt/%s/" % (vg_name, lv_name, lv_name), verbose=True)
    return ret


def _unmount_thin_lv(lv_name):
    ret = run("umount -f /mnt/%s/" % lv_name, verbose=True)
    ret += run("rm -rf /mnt/%s" % lv_name, verbose=True)
    return ret


def _metadata_snapshot(vg_name, lv_name):
    ret = run("dmsetup suspend /dev/mapper/%s-%s-tpool" % (vg_name, lv_name), verbose=True)
    ret += run("dmsetup message /dev/mapper/%s-%s-tpool 0 reserve_metadata_snap" % (vg_name, lv_name), verbose=True)
    ret += run("dmsetup resume /dev/mapper/%s-%s-tpool" % (vg_name, lv_name), verbose=True)
    return ret


def init(args):
    print("INFO: Initializing test case")
    errors = []

    atomic_run("Creating loopdev",
               expected_ret="/dev/loop1",
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

    # create few LVs to increase transaction ID and be able to do thin_delta
    for i in range(args["number of vols"]):
        atomic_run("Creating thin LV No. %s" % i,
                   vg_name=args["group"] + "/" + args["pool"],
                   lv_name=args["vol"] + str(i),
                   options=["-T", "-V 10"],
                   command=lv_create,
                   errors=errors)

        atomic_run("Mounting LV No. %s" % i,
                   expected_ret=0,
                   vg_name=args["group"],
                   lv_name=args["vol"] + str(i),
                   command=_mount_thin_lv,
                   errors=errors)

        atomic_run("Unmounting LV No. %s" % i,
                   expected_ret=0,
                   lv_name=args["vol"] + str(i),
                   command=_unmount_thin_lv,
                   errors=errors)

        atomic_run("Deactivating thin LV No. %s" % i,
                   lv_name=args["vol"] + str(i),
                   vg_name=args["group"],
                   command=lv_deactivate,
                   errors=errors)

    atomic_run("Creating metadata snapshot",
               expected_ret=0,
               lv_name=args["pool"],
               vg_name=args["group"],
               command=_metadata_snapshot,
               errors=errors)

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
        TC.tpass("Initialization passed")
    else:
        TC.tfail("Initialization failed with following errors: \n\t'" +
                 "\n\t ".join([str(i) for i in errors]))
        return 1
    return 0


def clean(args):
    print("INFO: Cleaning up")
    errors = []

    # restoring metadata device in case it is corrupted
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

    atomic_run("Removing swap",
               lv_name=args["swap"],
               vg_name=args["group"],
               command=lv_remove,
               errors=errors)

    atomic_run("Removing thinpool",
               lv_name=args["pool"],
               vg_name=args["group"],
               command=lv_remove,
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

    atomic_run("Deleting repair metadata file",
               cmd="rm -f /var/tmp/metadata_repair",
               command=run,
               errors=errors)

    atomic_run("Deleting snapshot metadata file",
               cmd="rm -f /var/tmp/metadata_snap",
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
    print("INFO: Testing thin tools runtime provided by device_mapper_persistent_data, iteration No. %s" %
          args["iteration"])

    errors = []

    atomic_run("Checking metadata",
               source_vg=args["group"],
               source_lv=args["swap"],
               command=thin_check,
               errors=errors)

    atomic_run("Checking metadata with few paramethers",
               source_vg=args["group"],
               source_lv=args["swap"],
               super_block_only=True,
               skip_mappings=True,
               ignore_non_fatal_errors=True,
               command=thin_check,
               errors=errors)

    atomic_run("Listing information about thin LVs",
               source_vg=args["group"],
               source_lv=args["swap"],
               command=thin_ls,
               errors=errors)

    atomic_run("Listing information about thin LVs without headers",
               source_vg=args["group"],
               source_lv=args["swap"],
               no_headers=True,
               command=thin_ls,
               errors=errors)

    atomic_run("Dumping metadata to standard output without mappings",
               formatting="human_readable",
               source_vg=args["group"],
               source_lv=args["swap"],
               skip_mappings=True,
               command=thin_dump,
               errors=errors)

    atomic_run("Dumping metadata to standard output",
               formatting="human_readable",
               source_vg=args["group"],
               source_lv=args["swap"],
               command=thin_dump,
               errors=errors)

    atomic_run("Dumping metadata to standard output from snapshot",
               formatting="human_readable",
               source_vg=args["group"],
               source_lv=args["swap"],
               snapshot=True,
               command=thin_dump,
               errors=errors)

    atomic_run("Dumping metadata with dev-id",
               formatting="human_readable",
               source_vg=args["group"],
               source_lv=args["swap"],
               dev_id=args["number of vols"] - 1,
               command=thin_dump,
               errors=errors)

    atomic_run("Calculating metadata size for pool of 64k blocks and 100M size",
               cmd="thin_metadata_size -b64k -s100m -m1 -um",
               command=run,
               errors=errors)

    atomic_run("Calculating metadata size for pool of 64k blocks and 100M size",
               cmd="thin_metadata_size -b64k -s100m -m1 -um -n",
               command=run,
               errors=errors)

    atomic_run("Calculating metadata size for pool of 64k blocks and 100M size",
               cmd="thin_metadata_size -b64k -s100m -m1 -um -nlong",
               command=run,
               errors=errors)

    atomic_run("Calculating metadata size for pool of 64k blocks and 100M size",
               cmd="thin_metadata_size -b64k -s100m -m1 -um -nshort",
               command=run,
               errors=errors)

    atomic_run("Outputting reverse map of metadata device",
               source_vg=args["group"],
               source_lv=args["swap"],
               region="0..-1",
               command=thin_rmap,
               errors=errors)

    atomic_run("Dumping metadata to file",
               formatting="xml",
               source_vg=args["group"],
               source_lv=args["swap"],
               repair=True,
               output="/var/tmp/metadata",
               command=thin_dump,
               errors=errors)

    atomic_run("Dumping metadata to file from snapshot",
               formatting="xml",
               source_vg=args["group"],
               source_lv=args["swap"],
               snapshot=True,
               output="/var/tmp/metadata_snap",
               command=thin_dump,
               errors=errors)

    atomic_run("Getting differences between thin LVs",
               source_vg=args["group"],
               source_lv=args["swap"],
               thin1=1,
               thin2=args["number of vols"] - 1,
               snapshot=True,
               command=thin_delta,
               errors=errors)

    atomic_run("Getting differences between thin LVs with --verbose",
               source_vg=args["group"],
               source_lv=args["swap"],
               thin1=1,
               thin2=args["number of vols"] - 1,
               verbosity=True,
               snapshot=True,
               command=thin_delta,
               errors=errors)

    atomic_run("Getting differences between the same LV",
               source_vg=args["group"],
               source_lv=args["swap"],
               thin1=1,
               thin2=1,
               snapshot=True,
               command=thin_delta,
               errors=errors)

    atomic_run("Getting differences between the same LV with --verbose",
               source_vg=args["group"],
               source_lv=args["swap"],
               thin1=1,
               thin2=1,
               verbosity=True,
               snapshot=True,
               command=thin_delta,
               errors=errors)

    atomic_run("Listing metadata output from snapshot",
               source_vg=args["group"],
               source_lv=args["swap"],
               snapshot=True,
               command=thin_ls,
               errors=errors)

    # need to run everything on snapshot before this as thin_restore removes the metadata snapshot
    # Restoring metadata from snapshot is not supported, see BZ1477232
    atomic_run("Restoring metadata to get 'couldn't zero superblock'",
               False,
               source_file="/var/tmp/metadata_snap",
               target_vg=args["group"],
               target_lv=args["swap"],
               command=thin_restore,
               errors=errors)

    atomic_run("Restoring metadata",
               source_file="/var/tmp/metadata",
               target_vg=args["group"],
               target_lv=args["swap"],
               command=thin_restore,
               errors=errors)

    atomic_run("Repairing metadata from file to get 'Metadata is not large enough for superblock'",
               False,
               pkg=["device-mapper-persistent-data", "0.7.3-3"],
               source_file="/var/tmp/metadata",
               target_vg=args["group"],
               target_lv=args["swap"],
               command=thin_repair,
               errors=errors)

    atomic_run("Repairing metadata to file",
               target_file="/var/tmp/metadata_repair",
               source_vg=args["group"],
               source_lv=args["swap"],
               command=thin_repair,
               errors=errors)

    atomic_run("Repairing metadata from file",
               source_file="/var/tmp/metadata_repair",
               target_vg=args["group"],
               target_lv=args["swap"],
               command=thin_repair,
               errors=errors)

    #   ##################### start of thin_trim #####################################
    # Need to swap back metadata to be able to activate thin pool
    atomic_run("Swapping metadata",
               vg_name=args["group"],
               lv_name=args["swap"],
               options=["-y", "--thinpool " + args["group"] + "/" + args["pool"],
                        "--poolmetadata "],
               command=lv_convert,
               errors=errors)

    atomic_run("Activating swap for thin_trim",
               lv_name=args["swap"],
               vg_name=args["group"],
               command=lv_activate,
               errors=errors)

    atomic_run("Activating pool for thin_trim",
               lv_name=args["pool"],
               vg_name=args["group"],
               command=lv_activate,
               errors=errors)

    # thin_trim requires activated thin pool and its metadata, that was required beforehand
    atomic_run("Discarding free space of pool",
               pkg=["device-mapper-persistent-data", "0.7.3-3"],
               data_vg=args["group"],
               data_lv=args["pool"],
               metadata_file="/var/tmp/metadata_repair",
               command=thin_trim,
               errors=errors)

    atomic_run("Deactivating pool after thin_trim",
               lv_name=args["pool"],
               vg_name=args["group"],
               command=lv_deactivate,
               errors=errors)

    atomic_run("Deactivating swap after thin_trim",
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

    atomic_run("Activating swap after thin_trim",
               lv_name=args["swap"],
               vg_name=args["group"],
               command=lv_activate,
               errors=errors)
    #   ##################### end of thin_trim #####################################

    atomic_run("Checking metadata",
               source_vg=args["group"],
               source_lv=args["swap"],
               command=thin_check,
               errors=errors)

    print("\n#######################################\n")

    if len(errors) == 0:
        TC.tpass("Testing thin tools of device_mapper_persistent_data passed, iteration No. %s" % args["iteration"])
    else:
        TC.tfail("Testing thin tools of device_mapper_persistent_data failed with following errors: \n\t'" +
                 "\n\t ".join([str(i) for i in errors]) +
                 "\nIteration No. %s" % args["iteration"])
        return 1
    return 0


def errors_test(args):
    print("\n#######################################\n")
    print("INFO: Testing thin tools errors provided by device_mapper_persistent_data, iteration No. %s" %
          args["iteration"])

    errors = []

    functions = ["thin_check", "thin_delta", "thin_dump", "thin_ls", "thin_metadata_size", "thin_repair",
                 "thin_restore", "thin_rmap", "thin_trim"]

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

    # Sanity to check present functions with -h
    for func in functions:
        if func in ["thin_trim"]:
            kwargs = {'pkg': ["device-mapper-persistent-data", "0.7.3-2"]}
        else:
            kwargs = {}
        atomic_run("Checking help of command",
                   cmd=func,
                   command=get_help,
                   errors=errors,
                   **kwargs)

    # Sanity to check present functions with -V
    for func in functions:
        if func in ["thin_trim", "thin_metadata_size"]:
            kwargs = {'pkg': ["device-mapper-persistent-data", "0.7.3-2"]}
        else:
            kwargs = {}
        atomic_run("Checking version of command",
                   cmd=func,
                   command=get_version,
                   errors=errors,
                   **kwargs)

    atomic_run("Checking original pool metadata, should fail",
               False,
               source_vg=args["group"],
               source_lv=args["pool"],
               command=thin_check,
               errors=errors)

    atomic_run("Listing information about thin LVs",
               False,
               cmd="thin_ls /dev/mapper/%s-%s --format \"WRONG\"" % (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Checking thin_metadata_size inputs",
               False,
               cmd="thin_metadata_size -b 64",
               command=run,
               errors=errors)

    atomic_run("Checking thin_metadata_size inputs",
               False,
               cmd="thin_metadata_size -b 64 -s 128",
               command=run,
               errors=errors)

    atomic_run("Checking thin_metadata_size inputs",
               False,
               cmd="thin_metadata_size -b 25 -s 128 -m 10",
               command=run,
               errors=errors)

    atomic_run("Checking thin_metadata_size inputs",
               False,
               cmd="thin_metadata_size -b 128 -s 64 -m 10",
               command=run,
               errors=errors)

    atomic_run("Checking thin_metadata_size inputs",
               False,
               cmd="thin_metadata_size -u h",
               command=run,
               errors=errors)

    atomic_run("Checking thin_metadata_size inputs",
               False,
               cmd="thin_metadata_size -n -n",
               command=run,
               errors=errors)

    atomic_run("Checking thin_metadata_size inputs",
               False,
               cmd="thin_metadata_size -nlongshort",
               command=run,
               errors=errors)

    atomic_run("Checking thin_metadata_size inputs",
               False,
               cmd="thin_metadata_size -b 128 -b 64",
               command=run,
               errors=errors)

    atomic_run("Repairing metadata without output",
               False,
               cmd="thin_repair -i /var/tmp/metadata_repair",
               command=run,
               errors=errors)

    atomic_run("Dumping metadata with wrong custom format",
               False,
               cmd="thin_dump /dev/mapper/%s-%s --format custom=wrong" % (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Dumping metadata with unknown format",
               False,
               cmd="thin_dump /dev/mapper/%s-%s --format wrong" % (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Dumping metadata with wrong dev-id",
               False,
               cmd="thin_dump /dev/mapper/%s-%s --dev-id wrong" % (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Repairing metadata to produce 'output file does not exist' error",
               False,
               cmd="thin_repair -i /dev/mapper/%s-%s -o /var/tmp/wrong.wrong" %
                   (args['group'], args['swap']),
               command=run,
               errors=errors)

    atomic_run("Repairing metadata to produce 'output file too small' error",
               False,
               cmd="thin_repair -i /var/tmp/metadata -o /var/tmp/metadata",
               command=run,
               errors=errors)

    atomic_run("Outputting reverse map of metadata device, should fail without region",
               False,
               pkg=["device-mapper-persistent-data", "0.7.3-2"],
               cmd="thin_rmap /dev/mapper/%s-%s" % (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Outputting reverse map of metadata device with bad region to get 'badly formed region (end <= begin)",
               False,
               cmd="thin_rmap /dev/mapper/%s-%s --region 0..0" % (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Outputting reverse map of metadata device with bad region to get "
               "'badly formed region (couldn't parse numbers)'",
               False,
               cmd="thin_rmap /dev/mapper/%s-%s --region 0...1" % (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Outputting reverse map of metadata device with bad region to get 'badly formed region (no dots)'",
               False,
               cmd="thin_rmap /dev/mapper/%s-%s --region 00" % (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Outputting reverse map of metadata device with wrong path to get 'Couldn't stat path'",
               False,
               cmd="thin_rmap --region 0..-1 /var/tmp/wrong.wrong",
               command=run,
               errors=errors)

    atomic_run("Outputting reverse map of metadata device to get 'Metadata is not large enough for superblock'",
               False,
               cmd="thin_rmap --region 0..-1 /var/tmp/metadata",
               command=run,
               errors=errors)

    atomic_run("Getting differences with thin1 ID out of range",
               False,
               source_vg=args["group"],
               source_lv=args["swap"],
               thin1=-1,
               thin2=args["number of vols"] - 1,
               command=thin_delta,
               errors=errors)

    atomic_run("Getting differences with thin2 ID out of range",
               False,
               source_vg=args["group"],
               source_lv=args["swap"],
               thin1=1,
               thin2=args["number of vols"] + 1,
               command=thin_delta,
               errors=errors)

    atomic_run("Restoring metadata without output",
               False,
               cmd="thin_restore -i /var/tmp/metadata",
               command=run,
               errors=errors)

    atomic_run("Restoring metadata with wrong options",
               False,
               cmd="thin_restore -i /var/tmp/metadata -o /dev/mapper/%s-%s --wrong test" % (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Restoring metadata with wrong source",
               False,
               cmd="thin_restore -i /var/tmp/wrong.wrong -o /dev/mapper/%s-%s" % (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Getting differences without thin2",
               False,
               cmd="thin_delta --thin1 1 /dev/mapper/%s-%s" %
                   (args["group"], args["swap"]),
               command=run,
               errors=errors)

    atomic_run("Corrupting metadata on device",
               cmd="echo 'nothing' >> /dev/mapper/%s-%s" %
                   (args['group'], args['swap']),
               command=run,
               errors=errors)

    atomic_run("Trying to fail while repairing metadata",
               False,
               source_vg=args['group'],
               source_lv=args['swap'],
               target_file="/var/tmp/metadata_repair",
               command=thin_repair,
               errors=errors)

    atomic_run("Trying to fail listing volumes",
               False,
               source_vg=args['group'],
               source_lv=args['swap'],
               command=thin_ls,
               errors=errors)

    atomic_run("Trying to fail while checking metadata",
               False,
               source_vg=args["group"],
               source_lv=args["swap"],
               command=thin_check,
               errors=errors)

    atomic_run("Trying to fail while dumping metadata from snapshot",
               False,
               formatting="human_readable",
               source_vg=args["group"],
               source_lv=args["swap"],
               snapshot=True,
               command=thin_dump,
               errors=errors)

    # restoring metadata device after corrupting it
    atomic_run("Repairing metadata device",
               source_file="/var/tmp/metadata",
               target_vg=args["group"],
               target_lv=args["swap"],
               quiet=True,
               command=thin_restore,
               errors=errors)

    print("\n#######################################\n")

    if len(errors) == 0:
        TC.tpass("Testing thin tools errors of device_mapper_persistent_data passed, iteration No. %s" %
                 args["iteration"])
    else:
        TC.tfail("Testing thin tools errors of device_mapper_persistent_data failed with following errors: \n\t'" +
                 "\n\t ".join([str(i) for i in errors]) +
                 "\nIteration No. %s" % args["iteration"])
        return 1
    return 0


def main():
    # Initialize Test Case
    global TC
    TC = stqe.host.tc.TestClass()

    args = {"loop": "loop1",
            "loop_size": 2048,
            "group": "vgtest",
            "pool": "thinpool",
            "vol": "thinvol",
            "number of vols": 10,
            "swap": "swapvol"}

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
