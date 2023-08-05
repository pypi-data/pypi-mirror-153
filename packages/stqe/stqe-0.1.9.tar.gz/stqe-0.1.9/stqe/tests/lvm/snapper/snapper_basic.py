#!/usr/bin/python

from __future__ import absolute_import, division, print_function, unicode_literals
from libsan.host.cmdline import run
from libsan.host.loopdev import create_loopdev, delete_loopdev
import libsan.host.lvm as lvm
import libsan.host.dm as dm
import libsan.host.linux as linux
import libsan.host.snapper as snapper
import stqe.host.beaker as beaker
import stqe.host.tc
import sys

#
# Bugs related:
#   BZ1365555 - Revert workaround for issues with snapper and btrfs subvolume labels
#

TestObj = None

loop_dev = None

vg_name = "vgtest"
pool_name = "test_pool"
thin1_name = "thin1"
brtfs_name = "brtfs_lv"
mnt_point_dev = "/mnt/snapper_test"
cfg_name = "bugtest"


def create_test_lv(filesystem):
    if not filesystem:
        return None

    # On brtfs we should not use thinp
    if filesystem != "btrfs":
        if run("lvcreate --thinpool %s -L 800M %s" % (pool_name, vg_name)) != 0:
            print("FAIL: Could not create %s - %s" % (pool_name, filesystem))
            return None
        if run("lvcreate -V 1G -T %s/%s -n %s" % (vg_name, pool_name, thin1_name)) != 0:
            print("FAIL: Could not create %s - %s" % (thin1_name, filesystem))
            return None

        return thin1_name
    else:
        if run("lvcreate -L 500M  -n %s %s" % (brtfs_name, vg_name)) != 0:
            print("FAIL: Could not create %s - %s" % (brtfs_name, filesystem))
            return None

        return brtfs_name


def start_test(filesystem, snapper_debug_mode):
    global TestObj

    print(80 * "#")
    print("INFO: Starting test on using snapper on %s debug mode:%s" % (filesystem, snapper_debug_mode))
    print(80 * "#")

    if snapper_debug_mode:
        # Wait 60 seconds so snapperd terminates
        linux.sleep(60)
        if not snapper.snapper_enable_debug_mode():
            TestObj.tfail("Could not enable snapper debug on FS(%s)" % filesystem)
            return False

    # create loop device of 900M
    global loop_dev
    loop_dev = create_loopdev(size=900)
    if not loop_dev:
        TestObj.tfail("Could not create loop device")
        return False

    if not lvm.vg_create(vg_name, loop_dev):
        TestObj.tfail("Could not create VG \"%s\"" % vg_name)
        return False

    print("INFO: Creating LVs")
    test_lv = create_test_lv(filesystem)
    if not test_lv:
        TestObj.tfail("Could not LV for FS(%s) with snapper_debug_mode=%s" % (filesystem, snapper_debug_mode))
        return False

    dm.dm_show_table()

    test_device = "/dev/mapper/%s-%s" % (vg_name, test_lv)
    print("INFO:Going to create FS(%s) on %s" % (filesystem, test_device))
    fs_option = ""
    if filesystem == "btrfs":
        # use mixed option as device is not big. more details see:
        # https://bugzilla.redhat.com/show_bug.cgi?id=1374158#c19
        fs_option = "--mixed"
    if run("mkfs.%s %s %s" % (filesystem, fs_option, test_device)) != 0:
        TestObj.tfail("Could not create FS(%s) on %s with snapper_debug_mode=%s"
                      % (filesystem, test_device, snapper_debug_mode))
        return False

    if not linux.mkdir(mnt_point_dev):
        TestObj.tfail("Could not create directory %s - FS(%s) with snapper_debug_mode=%s" % (
            mnt_point_dev, filesystem, snapper_debug_mode))
        return False

    if not linux.mount(test_device, mnt_point_dev):
        TestObj.tfail("Could not mount %s - FS(%s) with snapper_debug_mode=%s"
                      % (mnt_point_dev, filesystem, snapper_debug_mode))
        return False

    lvm.lv_show()

    print("INFO: Going create snapper config %s" % cfg_name)
    snap_type = "lvm(%s)" % filesystem
    if filesystem == "btrfs":
        snap_type = "btrfs"
    if not snapper.snapper_create_config(cfg_name, snap_type, mnt_point_dev):
        TestObj.tfail("Could not create snapper config - FS(%s) with snapper_debug_mode=%s"
                      % (filesystem, snapper_debug_mode))
        return False

    run("ps -ef | grep snapper")

    if not snapper.snapper_list_configs():
        TestObj.tfail("Could not list config FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    # list current snapshots
    # do not expect any snaphost to be listed
    if not snapper.snapper_list(cfg_name):
        TestObj.tfail("Could not list snapshots FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    print("INFO: Creating single snapshot")
    pre_num = snapper.snapper_create(cfg_name, "single")
    if not pre_num:
        TestObj.tfail("Could not create SINGLE snapshot FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    if not linux.mkdir("%s/dir_0" % mnt_point_dev):
        TestObj.tfail("Could not create directory on %s - FS(%s) with snapper_debug_mode=%s" % (
            mnt_point_dev, filesystem, snapper_debug_mode))
        return False
    if run("touch %s/dir_0/file_0" % mnt_point_dev) != 0:
        TestObj.tfail("Could not ecreate file FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    print("INFO: Creating pre snapshot")
    pre_num = snapper.snapper_create(cfg_name, "pre")
    if not pre_num:
        TestObj.tfail("Could not create PRE snapshot FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    if not snapper.snapper_list(cfg_name):
        TestObj.tfail("Could not list snapshots FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    print("INFO: Creating data on %s" % mnt_point_dev)
    if not linux.mkdir("%s/dir_1" % mnt_point_dev):
        TestObj.tfail("Could not create directory on %s - FS(%s) with snapper_debug_mode=%s" % (
            mnt_point_dev, filesystem, snapper_debug_mode))
        return False
    if run("touch %s/dir_1/file_1" % mnt_point_dev) != 0:
        TestObj.tfail("Could not create file FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False
    if run("echo \"going to create snapshot\" >> %s/dir_0/file_0" % mnt_point_dev) != 0:
        TestObj.tfail("Could not edit file FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    print("INFO: Creating post snapshot")
    post_num = snapper.snapper_create(cfg_name, "post", pre_num=pre_num)
    if not post_num:
        TestObj.tfail("Could not create POST snapshot FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    if not snapper.snapper_list(cfg_name):
        TestObj.tfail("Could not list snapshots FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    if not snapper.snapper_status(cfg_name, pre_num, post_num):
        TestObj.tfail("Could not get status for snapshots FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    if not snapper.snapper_diff(cfg_name, pre_num, post_num):
        TestObj.tfail("Could not get diff for snapshots FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    print("INFO: Deleting post snapshot")
    if not snapper.snapper_delete(cfg_name, post_num):
        TestObj.tfail("Could not delete POST snapshot FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    if not snapper.snapper_list(cfg_name):
        TestObj.tfail("Could not list snapshots FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    print("INFO: Deleting pre snapshot")
    if not snapper.snapper_delete(cfg_name, pre_num):
        TestObj.tfail("Could not delete PRE snapshot FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    print("INFO: Deleting config")
    if not snapper.snapper_delete_config(cfg_name):
        TestObj.tfail("Could not delete config FS(%s) on %s with snapper_debug_mode=%s" % (
            filesystem, test_device, snapper_debug_mode))
        return False

    # Wait 60 seconds so snapperd terminates
    linux.sleep(60)
    if snapper_debug_mode:
        if not snapper.snapper_disable_debug_mode():
            TestObj.tfail("Could not disable snapper debug on FS(%s)" % filesystem)
            return False

    print(80 * "#")
    TestObj.tpass("PASS: Test on FS %s and snapper_debug_mode=%s" % (filesystem, snapper_debug_mode))
    print(80 * "#")

    return True


def _clean_up():
    global vg_name, loop_dev

    snapper.snapper_delete_config(cfg_name)

    linux.umount(mnt_point_dev)

    # make sure any failed device is removed
    if not lvm.vg_remove(vg_name, force=True):
        TestObj.tfail("Could not delete VG \"%s\"" % vg_name)

    if loop_dev:
        if not lvm.pv_remove(loop_dev):
            TestObj.tfail("Could not delete PV \"%s\"" % loop_dev)
        delete_loopdev(loop_dev)


def execute_test():
    global TestObj

    os_version = linux.dist_ver()
    os_name = linux.dist_name()

    if os_name == "RHEL" and os_version < 7:
        TestObj.tskip("Test is not supported on %s-%s" % (os_name, os_version))
        return

    linux.install_package("snapper")

    filesystems = ["ext4", "xfs"]
    # btrfs is depreciated in RHEL 7.4, but should remain accessible in RHEL 7 series
    # also btrfs was purposely removed from Pegas Kernel (RHEL ALT)
    ret, kernel = run(cmd='uname -r', return_output=True)
    if ret:
        print("WARN: Could not get kernele version, running without btrfs.")
    else:
        version = kernel.split("-")[0].split(".")
        # FIXME: add check for RHEL < 8
        if int(version[0]) <= 4 and int(version[1]) <= 11:
            filesystems.append("btrfs")
    # test using snapperd with and without debug
    dbg_modes = [False, True]

    for fs in filesystems:
        for dbg_mode in dbg_modes:
            _clean_up()

            if not start_test(fs, dbg_mode):
                log_name = "snapper_%s_%s.log" % (fs, dbg_mode)
                run("mv /var/log/snapper.log %s" % log_name)
                beaker.log_submit(log_name)

    _clean_up()
    return


def main():
    global TestObj

    TestObj = stqe.host.tc.TestClass()

    linux.install_package("snapper")
    linux.install_package("lvm2")

    execute_test()

    if not TestObj.tend():
        print("FAIL: test failed")
        sys.exit(1)

    print("PASS: Test pass")
    sys.exit(0)


main()
