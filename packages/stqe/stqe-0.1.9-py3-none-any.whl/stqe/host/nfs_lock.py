from __future__ import absolute_import, division, print_function, unicode_literals

# Copyright (C) 2016 Red Hat, Inc.
# python-stqe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-stqe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-stqe.  If not, see <http://www.gnu.org/licenses/>.

"""mfs_lock.py: Module to handle storage reservation using NFS."""

import re  # regex
import os
import libsan.host.linux
import libsan.sanmgmt
import libsan.host.iscsi as iscsi
import stqe.host.beaker as beaker
from libsan.host.cmdline import run

"""
The idea is kind complex.
1. Data structures
1.1 Queue Data:
All servers that want use a storage device need to request it.
The request is added to the queue data.
During the request it is informed if host wants to use the storage device exclusively or shared
1.2 Lock Data:
1.2.1 Lock data contains all hosts that are locked the storage_device.
1.2.2 Lock data can have more than 1 entry there if they are all shared
1.2.3 Exclusive lock can only be added when lock data is empty, only 1 entry per time

2. Moving data from Queue to Lock data
2.1 If there is exclusive lock on queue, try to add it to lock data
2.1.1 If lock data is empty, lock is added
2.1.2 If lock data is not empty the exclusive request remains on queue until Lock data is free
2.2 If there is shared request and no exclusive request
2.2.1 There is no exclusive lock on Lock data, shared lock is added to Lock data
2.2.2 If Lock data has exclusive lock, need to wait lock data to be empty

3. Need to guaranty exclusive access to NFS files
3.1 To do that there is an update_token. The host that gets it can change lock data and queue data
3.2 Prior any change on Data structures we need to make sure we got the update_token

4. Usage:
4.1 nfs_lock = libsan.host.nfs_lock.nfs_lock("server","share","mount_point","storage_name")
4.2 nfs_lock.request_lock("shared")
4.3 nfs_lock.get_lock() #It blocks until get the lock
4.4 nfs_lock.release_lock("shared")
"""

__author__ = "Bruno Goncalves"
__copyright__ = "Copyright (c) 2016 Red Hat, Inc. All rights reserved."


def _print(string):
    module_name = __name__
    string = re.sub("DEBUG:", "DEBUG:(" + module_name + ") ", string)
    string = re.sub("FAIL:", "FAIL:(" + module_name + ") ", string)
    string = re.sub("FATAL:", "FATAL:(" + module_name + ") ", string)
    string = re.sub("WARN:", "WARN:(" + module_name + ") ", string)
    print(string)
    if "FATAL:" in string:
        raise RuntimeError(string)
    return


def _read_file(file_path):
    """
    """
    while True:
        try:
            if not os.path.isfile(file_path):
                return None
            f = open(file_path)
            break
        except Exception as e:
            print(e)
            _print("FAIL: _read_file() - Could not open %s" % file_path)
            libsan.host.linux.sleep(5)
    if not f:
        _print("FAIL: _read_file() - Could not open %s" % file_path)
        return None

    try:
        file_data = f.read()
    except Exception as e:
        print(e)
        # Maybe due Stale IO, like the path has been deleted...
        _print("FAIL: _read_file() - Could not read %s" % file_path)
        f.close()
        return None
    f.close()
    if not file_data:
        return None
    file_lines = file_data.split("\n")
    if not file_lines:
        return None

    return_lines = []
    # Remove empty lines
    for line in file_lines:
        if line != "":
            return_lines.append(line)

    return return_lines


def _delete_item_queue_file(file_path, item_str):
    """
    """
    _print("DEBUG: Deleting %s from %s" % (item_str, file_path))

    queue_info = _read_file(file_path)
    if not queue_info:
        _print("FAIL: Could not read %s" % file_path)
        return False

    try:
        f = open(file_path, "w")
    except Exception as e:
        print(e)
        _print("FAIL: _delete_item_queue_file() - Could not open %s" % file_path)
        return False
    for line in queue_info:
        if line != item_str:
            f.write("%s\n" % line)
    f.close()
    return True


def setup_nfs_lock_for_mpath(mpath_name):
    """
    To avoid race condition when performing disruptive action on Storage array
    We use NFS as lock mechanism
    Return:
    \tNFS lock object
    """
    if not mpath_name:
        _print("FAIL: setup_nfs_lock_for_mpath() - requires mpath_name as parameter")
        return None

    obj_libsan = libsan.sanmgmt.create_sanmgmt_for_mpath(mpath_name)
    if not obj_libsan:
        _print("FAIL: setup_nfs_lock_for_mpath() - Could not create libsan for %s" % mpath_name)
        return None

    general_conf_dict = None
    if "general" in obj_libsan.san_conf_dict:
        general_conf_dict = obj_libsan.san_conf_dict["general"]

    if not general_conf_dict:
        _print("FAIL: Could not set NFS lock. It is not configured on san config file")
        print(obj_libsan.san_conf_dict)
        return None

    if "nfs_server" not in general_conf_dict:
        _print("WARN: setup_nfs_lock_for_mpath() - nfs_server is not "
               "configured on SAN config file, under general section")
        print(general_conf_dict)
        return None

    if "nfs_share" not in general_conf_dict:
        _print("WARN: setup_nfs_lock_for_mpath() - nfs_share is not configured "
               "on SAN config file, under general section")
        print(general_conf_dict)
        return None

    if "nfs_mount_point" not in general_conf_dict:
        _print("WARN: setup_nfs_lock_for_mpath() - nfs_mount_point is not "
               "configured on SAN config file, under general section")
        print(general_conf_dict)
        return None

    sa = obj_libsan.get_sa_self()
    if not sa:
        _print("FAIL: setup_nfs_lock_for_mpath() - Could not find Storage "
               "Array managed by libsan")
        return None

    if "lock_array_name" not in sa:
        _print("FAIL: setup_nfs_lock_for_mpath() - lock_array_name is not defined "
               "under array section on SAN config file")
        print(sa)
        return None
    lock_obj = NfsLock(general_conf_dict["nfs_server"], general_conf_dict["nfs_share"],
                       general_conf_dict["nfs_mount_point"], "%s" % sa["lock_array_name"])
    mount_point = general_conf_dict["nfs_mount_point"]
    if not os.path.isdir(mount_point):
        if not libsan.host.linux.mkdir(mount_point):
            _print("FAIL: Could not create %s" % mount_point)
            return None

    libsan.host.linux.umount(general_conf_dict["nfs_mount_point"])
    if not lock_obj.mount_lock():
        return None
    return lock_obj


def setup_nfs_lock_lun(obj_sangmtm, wwid, nfs_lock_type):
    """
    Lock whole storage array with 'shared' lock and lock LUN on the array with nfs_lock_type lock
    :param obj_sangmtm: libsan.sangmtm.SanMgmt dict with information about the storage array
    :param wwid: wwid of LUN to lock
    :param nfs_lock_type: lock type ['shared', 'exclusive'] of the LUN
    :return: True | False
    """
    general_conf_dict = obj_sangmtm.san_conf_dict["general"]
    sa = obj_sangmtm.get_sa_self()
    if not sa:
        _print("FAIL: setup_nfs_lock_lun() - there is no array configured for given sanmgmt config.")
        return False

    # create shared lock on storage array
    _print("INFO: setup_nfs_lock_lun() - creating 'shared' lock on storage array")
    lock_obj_sa = NfsLock(general_conf_dict["nfs_server"], general_conf_dict["nfs_share"],
                          general_conf_dict["nfs_mount_point"], "%s" % sa["lock_array_name"])

    mount_point = general_conf_dict["nfs_mount_point"]
    if not os.path.isdir(mount_point):
        if not libsan.host.linux.mkdir(mount_point):
            _print("FAIL: Could not create %s" % mount_point)
            return None
    libsan.host.linux.umount(general_conf_dict["nfs_mount_point"])
    if not lock_obj_sa.mount_lock():
        return None

    # add shared lock to the storage array as we are locking just one LUN
    if not lock_obj_sa.request_lock("shared"):
        _print("FAIL: setup_nfs_lock_lun() - could not request lock on storage array.")
        return False
    # need to wait on lock before we can proceed
    _print("INFO: Storage array lock request added to queue, starting to wait on lock.")
    if not lock_obj_sa.get_lock():
        _print("FAIL: setup_nfs_lock_lun() - could not get lock on storage array.")
        return False
    _print("INFO: setup_nfs_lock_lun() - storage array locked - 'shared'")

    # add lock to the LUN
    _print("INFO: setup_nfs_lock_lun() - creating '%s' lock for LUN '%s'" % (nfs_lock_type, wwid))
    lock_obj_lun = NfsLock(general_conf_dict["nfs_server"], general_conf_dict["nfs_share"],
                           general_conf_dict["nfs_mount_point"], "%s" % sa["lock_array_name"] + "/" + wwid)
    if not lock_obj_lun.request_lock(nfs_lock_type):
        _print("FAIL: setup_nfs_lock_lun() - could not request lock on LUN.")
        return False

    _print("INFO: NFS lock request added to queue, starting to wait on lock.")
    if not lock_obj_lun.get_lock():
        _print("FAIL: setup_nfs_lock_lun() - could not get lock on LUN.")
        return False
    _print("INFO: setup_nfs_lock_lun() - LUN locked - '%s'" % nfs_lock_type)
    return True


def release_nfs_lock_lun(obj_sanmgmt, wwid, nfs_lock_type):
    """
    Relase lock from whole storage array and LUN on the array with nfs_lock_type lock
    :param obj_sangmtm: libsan.sangmtm.SanMgmt dict with information about the storage array
    :param wwid: wwid of LUN to unlock
    :param nfs_lock_type: lock type ['shared', 'exclusive'] of the LUN
    :return: True | False
    """
    general_conf_dict = obj_sanmgmt.san_conf_dict["general"]
    sa = obj_sanmgmt.get_sa_self()
    if not sa:
        _print("FAIL: setup_nfs_lock_lun() - there is no array configured for given sanmgmt config.")
        return False

    # release lock from the LUN
    _print("INFO: release_nfs_lock_lun - releasing LUN '%s' lock" % nfs_lock_type)
    lock_obj_lun = NfsLock(general_conf_dict["nfs_server"], general_conf_dict["nfs_share"],
                           general_conf_dict["nfs_mount_point"], "%s" % sa["lock_array_name"] + "/" + wwid)
    if not lock_obj_lun.release_lock(nfs_lock_type):
        _print("FAIL: release_nfs_lock_lun() - could not release lock on LUN '%s', trying again." % wwid)
        lock_obj_lun.release_lock(nfs_lock_type, 10)
        # do not return here, we still need to clear lock on storage array
    _print("INFO: release_nfs_lock_lun() - LUN lock '%s' released" % nfs_lock_type)

    # release shared lock on storage array
    _print("INFO: release_nfs_lock_lun() - removing 'shared' lock on storage array")
    lock_obj_sa = NfsLock(general_conf_dict["nfs_server"], general_conf_dict["nfs_share"],
                          general_conf_dict["nfs_mount_point"], "%s" % sa["lock_array_name"])
    if not lock_obj_sa.release_lock("shared"):
        _print("FAIL: release_nfs_lock_lun() - could not release lock on storage array, trying again.")
        if not lock_obj_sa.release_lock("shared", 10):
            return False
    _print("INFO: release_nfs_lock_lun() - storage array lock 'shared' released")
    return True


def _get_iscsi_params(sid):
    """
    Loads params from iscsi to sanmgmt dict and returns it.
    :param iqn: iscsi iqn to get params about
    :return: dict loaded sanmgmgt | None
    """
    iscsi_session = iscsi.query_iscsi_session(sid)
    if not iscsi_session:
        _print("FAIL: setup_nfs_lock_for_iscsi() - could not fid iscsi session sid '%s'" % sid)
        return None

    h_iqn = iscsi_session["h_iqn"]
    t_iqn = iscsi_session["t_iqn"]
    iface_mac = iscsi_session["mac"]
    map_info = {"t_iqn": t_iqn, "h_iqn": h_iqn}

    obj_libsan = libsan.sanmgmt.SanMgmt()
    obj_libsan.map_info(map_info)
    obj_libsan.h_iqns([h_iqn])
    obj_libsan.t_iqns([t_iqn])
    obj_libsan.macs([iface_mac])
    obj_libsan.load_conf()
    return obj_libsan


def setup_nfs_lock_iscsi(disk_name, nfs_lock_type="exclusive"):
    """
    Create lock on iscsi LUN and 'shared' lock on its storage array.
    :param disk_name: disk to lock (for example 'sdd')
    :param nfs_lock_type: lock type ['shared', 'exclusive'] of the LUN
    :return: True | False
    """

    if not disk_name:
        _print("FAIL: setup_nfs_lock_iscsi() - requires disk_name as parameter")
        return False

    sid = libsan.host.iscsi.get_session_id_from_disk(disk_name)
    wwid = libsan.host.scsi.wwid_of_disk(disk_name)
    _print("INFO: setup_nfs_lock_iscsi() - locking wwid '%s' on sid '%s'" % (wwid, sid))

    obj_libsan = _get_iscsi_params(sid)
    if not obj_libsan:
        _print("FAIL: setup_nfs_lock_iscsi() - could not find sid %s in iscsi sessions" % sid)
        return False

    if not setup_nfs_lock_lun(obj_libsan, wwid, nfs_lock_type):
        _print("FAIL: setup_nfs_lock_iscsi() - could not setup lock for iscsi LUN.")
        return False
    return True


def release_nfs_lock_iscsi(disk_name, nfs_lock_type="exclusive"):
    """
    Removes nfs_lock_type lock on iscsi LUN and 'shared' lock on storage array.
    :param iqn: IQN of LUN to lock
    :param nfs_lock_type: lock type ['shared', 'exclusive']
    :return: True | False
    """
    if not disk_name:
        _print("FAIL: release_nfs_lock_iscsi() - requires iqn as parameter")
        return None

    sid = libsan.host.iscsi.get_session_id_from_disk(disk_name)
    wwid = libsan.host.scsi.wwid_of_disk(disk_name)

    obj_libsan = _get_iscsi_params(sid)
    if not obj_libsan:
        _print("FAIL: release_nfs_lock_iscsi() - could not find sid '%s' in iscsi sessions" % sid)
        return False

    if not release_nfs_lock_lun(obj_libsan, wwid, nfs_lock_type):
        _print("FAIL: release_nfs_lock_iscsi() - could not release lock for iscsi LUN.")
        return False
    return True


class NfsLock(object):
    """
    Class to manage NFS Lock
    """
    _nfs_server = None
    _nfs_export = None
    _mount_point = None
    _device_name = None
    _directory_path = None

    _monitor_pid = None

    _queue_file = "queue_file"
    _queue_file_path = None

    _lock_file = "lock_file"
    _lock_file_path = None

    # As NFS does not handle well multiple access to a file
    # We will try to make sure only 1 server has access to the lock info at same time
    _update_token_file = "update_token"
    _update_token_file_path = None

    # Queue has hostname and lock_type info
    _queue_format_regex = re.compile(r"^(\S+) lock_type: (\S+) time: (\S+) task_id: (\S+)")
    _lock_format_regex = re.compile(r"^(\S+)\s(\S+)\s(\S+)\s(\S+)")

    supported_lock_types = ["shared", "exclusive"]

    def __init__(self, nfs_server, nfs_export, mount_point, storage_name):
        """
        """
        if not nfs_server:
            raise ValueError("FAIL: __init__() - requires nfs_server parameterr")

        if not nfs_export:
            raise ValueError("FAIL: __init__() - requires nfs_export parameter")

        if not mount_point:
            raise ValueError("FAIL: __init__() - requires mount_point parameter")

        if not storage_name:
            raise ValueError("FAIL: __init__() - requires storage_name parameter")

        self._nfs_server = nfs_server
        self._nfs_export = nfs_export
        self._mount_point = mount_point
        self._device_name = storage_name

        self._directory_path = "%s/%s" % (mount_point, storage_name)

        self._queue_file_path = "%s/%s" % (self._directory_path, self._queue_file)
        self._lock_file_path = "%s/%s" % (self._directory_path, self._lock_file)
        self._update_token_file_path = "%s/%s" % (self._directory_path, self._update_token_file)

    def mount_lock(self):
        """
        Mount NFS lock export
        """
        src = "%s:%s" % (self._nfs_server, self._nfs_export)
        if not libsan.host.linux.mount(src, self._mount_point, fs="nfs"):
            _print("FAIL: Could not mount %s:%s" % (self._nfs_server, self._nfs_export))
            return False
        return True

    def umount_lock(self):
        """
        umount NFS lock export
        """
        if not libsan.host.linux.umount(self._mount_point):
            _print("FAIL: Could not umount %s" % self._mount_point)
            return False
        return True

    #   ########## UPDATE TOKEN ############
    def get_update_token(self):
        """
        Waits until we get the right to update the NFS folder
        """
        _print("INFO: Waiting to get update token")
        if not os.path.isdir(self._directory_path):
            if not libsan.host.linux.mkdir(self._directory_path):
                _print("FATAL: Could not create directory: %s" % self._directory_path)
                return False
            # Sync after creating the directory
            libsan.host.linux.sync(self._directory_path)

        got_token = False
        update_token_regex = re.compile(r"^(\S+) (\S+)")
        count = 0
        previous_token = None
        elapsed_time = 0
        while not got_token:
            if not os.path.isfile(self._update_token_file_path):
                # It seems we can get access to update NFS directory
                token_info = "%s %s" % (libsan.host.linux.hostname(),
                                        libsan.host.linux.time_stamp(in_seconds=True))
                run("echo %s >> %s" % (token_info, self._update_token_file_path))
                libsan.host.linux.sync(self._directory_path)
                libsan.host.linux.sleep(10)
                libsan.host.linux.sync(self._directory_path)
                token = _read_file(self._update_token_file_path)
                if not token or (len(token) > 1):
                    _print("FAIL: It seems we got concurrent access to update token. "
                           "Deleting it...")
                    run("rm -f %s" % self._update_token_file_path)
                    libsan.host.linux.sync(self._directory_path)
                    continue
                m = update_token_regex.match(token[0])
                if not m:
                    _print("FAIL: %s is not valid token" % token[0])
                    run("rm -f %s" % self._update_token_file_path)
                    libsan.host.linux.sync(self._directory_path)
                _print("INFO: We got the update token!")
                return token
            else:
                token = _read_file(self._update_token_file_path)
                if not token or (previous_token != token):
                    # token changed, we should refresh counter
                    elapsed_time = 0
                    previous_token = token

                if elapsed_time > 60:
                    _print("FAIL: timeout expired for update token. Deleting it...")
                    run("rm -f %s" % self._update_token_file_path)
                    libsan.host.linux.sync(self._directory_path)

                if count >= 5:
                    _print("INFO: Still waiting for update token...")
                    count = 0
                # Sleep a bit before checking for the token again
                libsan.host.linux.sleep(1)
                count += 1
                elapsed_time += 1

    def release_update_token(self):
        """
        Release the update token
        """
        libsan.host.linux.sync(self._directory_path)
        if os.path.isdir(self._directory_path):
            if os.path.isfile(self._update_token_file_path):
                run("rm -f %s" % self._update_token_file_path)
                libsan.host.linux.sync(self._directory_path)
                return True
        return False

    #       ############# QUEUE ########################

    def _add_queue(self, host, lock_type):
        """
        Add lock request to the queue
        """

        if not os.path.isdir(self._directory_path):
            if not libsan.host.linux.mkdir(self._directory_path):
                _print("FAIL: _add_queue() - Could not create %s" % self._directory_path)
                return False

        if not host or not lock_type:
            _print("FAIL: _add_queue() - requires host and lock_type parameters")
            return False

        if not libsan.host.linux.sync(self._directory_path):
            _print("FAIL: Could not sync %s" % self._directory_path)
            return None

        queue_data = _read_file(self._queue_file_path)
        beaker_task_id = None
        if "TASKID" in os.environ:
            beaker_task_id = os.environ['TASKID']
        if not beaker_task_id:
            # TODO
            beaker_task_id = "manual"
        device_info = "%s lock_type: %s time: %s task_id: %s" % (host, lock_type,
                                                                 libsan.host.linux.time_stamp(in_seconds=True),
                                                                 beaker_task_id)
        if queue_data:
            for queue_device in queue_data:
                m = self._queue_format_regex.match(queue_device)
                if not m:
                    _print("FAIL: '%s' does not match a queue entry format" % queue_device)
                    _delete_item_queue_file(self._queue_file_path, queue_device)
                    continue
                if m.group(1) == host:
                    _print("INFO: Deleting previous entry for host %s (%s)" % (host, queue_device))
                    _delete_item_queue_file(self._queue_file_path, queue_device)

        # Open file for write with append
        f = open(self._queue_file_path, "a")
        if not f:
            _print("FAIL: _add_queue() - Could not open %s" % self._queue_file_path)
            return False

        try:
            f.write("%s\n" % device_info)
            f.close()
        except Exception as e:
            print(e)
            _print("FAIL: _add_queue() - Could not add %s to queue" % host)
            f.close()
            return False

        if not libsan.host.linux.sync(self._directory_path):
            _print("FAIL: Could not sync %s" % self._directory_path)
            return None
        return True

    def _dequeue(self):
        """
        Remove a lock request from queue
        """
        _print("INFO: Updating queue and lock lists")
        if not os.path.isdir(self._directory_path):
            # It seems no lock has ever been queued to this device
            _print("INFO: There is not directory %s" % self._directory_path)
            return None

        if not os.path.isfile(self._queue_file_path):
            _print("DEBUG: _dequeue() -  %s does not exist" % self._queue_file_path)
            return None

        if not libsan.host.linux.sync(self._directory_path):
            _print("FAIL: Could not sync %s" % self._directory_path)
            return None

        queue_devices = _read_file(self._queue_file_path)
        if not queue_devices:
            _print("DEBUG: _dequeue() - there is no host queued for %s" % self._device_name)
            return None

        # list of devies that should be add to lock file and removed from queue
        devices_2_lock = []
        # If first entry is shared we can lock more devices that also
        # request for shared access
        # if first entry is exclusive we just add it to lock
        _print("DEBUG: _dequeue() - queue devices:")
        print(queue_devices)

        # Check if there is requests queued for long time
        # If there is the queue will contain only these requests
        wait_long_devs = []
        for queue_device in queue_devices:
            _print("DEBUG: _dequeue() - checking if request is waiting for long time in queue: '%s'" % queue_device)
            m = self._queue_format_regex.match(queue_device)
            if not m:
                _print("FAIL: '%s' does not match a queue entry format" % queue_device)
                _delete_item_queue_file(self._queue_file_path, queue_device)
                queue_devices.remove(queue_device)
                continue
            current_timestamp = int(libsan.host.linux.time_stamp(in_seconds=True))
            timeout = int(m.group(3)) + (60 * 60)
            # If a request has not been queued for more than 1h it is not queued long enough
            # to get higher priority
            if current_timestamp < timeout:
                continue
            processing_lock_type = m.group(2)
            if processing_lock_type == "exclusive":
                # Just add the exclusive device
                wait_long_devs = [queue_device]
                break
            wait_long_devs.append(queue_device)
        if wait_long_devs:
            queue_devices = wait_long_devs
        # Check if there is any server waiting for exclusive access
        # They have priority
        for queue_device in queue_devices:
            _print("DEBUG: _dequeue() - checking for exclusive lock in queue: '%s'" % queue_device)
            m = self._queue_format_regex.match(queue_device)
            if not m:
                _print("FAIL: '%s' does not match a lock entry format" % queue_device)
                _delete_item_queue_file(self._queue_file_path, queue_device)
                queue_devices.remove(queue_device)
                continue
            processing_lock_type = m.group(2)
            if processing_lock_type == "exclusive":
                devices_2_lock.append(queue_device)
                break
        # If there is no exclusive request
        if not devices_2_lock:
            for queue_device in queue_devices:
                _print("DEBUG: _dequeue() - checking for shared lock in queue: '%s'" % queue_device)
                m = self._queue_format_regex.match(queue_device)
                if not m:
                    _print("FAIL: '%s' does not match a lock entry format" % queue_device)
                    _delete_item_queue_file(self._queue_file_path, queue_device)
                    queue_devices.remove(queue_device)
                    continue
                processing_lock_type = m.group(2)
                if processing_lock_type == "shared":
                    devices_2_lock.append(queue_device)
                    continue

        if not devices_2_lock:
            _print("DEBUG: _dequeue() - there is no lock device pending for %s" % self._device_name)
            return None

        for device in devices_2_lock:
            m = self._queue_format_regex.match(device)
            if not m:
                _print("FAIL: _dequeue() - device %s is not on proper format" % device)
                self.show_queue()
                return None
            if not self._add_lock(m.group(1), m.group(2), m.group(4)):
                _print("FAIL: _dequeue() - Could not add %s to lock file" % device)
                return None
            # device success fully added to lock, remove it from queue
            _delete_item_queue_file(self._queue_file_path, device)

        if not libsan.host.linux.sync(self._directory_path):
            _print("FAIL: Could not sync %s" % self._directory_path)
            return None
        _print("DEBUG: _dequeue() - Servers locked using %s are:" % self._device_name)
        self.show_lock()
        return devices_2_lock

    #   ########## LOCK ###################
    def show_queue(self):
        """
        Show lock queue
        """
        _print("INFO: ### Showing NFS queue data #########")
        cmd = "cat %s " % self._queue_file_path
        ret, output = run(cmd, return_output=True, verbose=False)
        print(output)
        _print("INFO: ### End NFS queue data #########")
        return True

    def request_lock(self, lock_type):
        """
        Add this lock request to lock queue
        """
        host = libsan.host.linux.hostname()
        _print("INFO: Requesting %s lock for %s" % (lock_type, host))

        if not lock_type:
            _print("FAIL: request_lock() - requires lock_type parameters")
            return False

        if lock_type not in self.supported_lock_types:
            _print("FAIL: %s is not a supported lock type" % lock_type)
            return False

        # Waiting for update token
        self.get_update_token()

        if not self._add_queue(host, lock_type):
            _print("FAIL: request_lock() - Could not lock request to queue")
            self.release_update_token()
            return False
        _print("INFO: Added lock request to queue")
        self.release_update_token()
        self.show_queue()
        return True

    def _add_lock(self, host, lock_type, beaker_task_id):
        """
        Set the host
        """

        if not os.path.isdir(self._directory_path):
            if not libsan.host.linux.mkdir(self._directory_path):
                _print("FAIL: _add_lock() - Could not create %s" % self._directory_path)
                return False

        if not host or not lock_type or not beaker_task_id:
            _print("FAIL: _add_lock() - requires host, lock_type and task_id parameters")
            return False

        if not libsan.host.linux.sync(self._directory_path):
            _print("FAIL: Could not sync %s" % self._directory_path)
            return False

        lock_data = _read_file(self._lock_file_path)
        if not beaker_task_id:
            # TODO
            beaker_task_id = "manual"
        device_info = "%s %s %s %s" % (host, lock_type,
                                       libsan.host.linux.time_stamp(in_seconds=True),
                                       beaker_task_id)
        _print("DEBUG: _add_lock() - Adding %s to lock data:" % device_info)
        print(lock_data)
        if lock_data:
            # In case we got a "exclusive" lock request, but lock data is not empty, we will not
            # add it to lock data
            if lock_type == "exclusive":
                _print("INFO: There is an exclusive lock request on queue, "
                       "but lock data is not empty. Need to wait lock data to get empty first...")
                self.show_lock()
                return False

            for locked_host in lock_data:
                # _print("DEBUG: _add_lock() - Checking if %s match on %s" % (host, locked_host))
                m = self._lock_format_regex.match(locked_host)
                if not m:
                    # TODO
                    _print("WARN: _add_lock() - %s is not valid lock host entry. "
                           "Deleting it..." % locked_host)
                    _delete_item_queue_file(self._lock_file_path, locked_host)
                    continue
                if m.group(1) == host:
                    _print("INFO: %s already locked" % host)
                    return True
                if m.group(2) == "exclusive":
                    _print("INFO: Storage device is locked exclusively. "
                           "Need to wait Lock to get empty first...")
                    return False

        # Open file for write with append
        ret, output = run("echo %s >> %s" % (device_info, self._lock_file_path),
                          return_output=True, verbose=False)
        if ret != 0:
            _print("FAIL: _add_lock() - Could not write to %s" % self._lock_file_path)
            print(output)
            return False

        if not libsan.host.linux.sync(self._directory_path):
            _print("FAIL: Could not sync %s" % self._directory_path)
            return False
        _print("DEBUG: _add_lock() - Added %s to lock data" % device_info)
        return True

    def check_lock(self):
        """
        Check which servers are using the device
        """

        _print("INFO: Checking lock status")
        if not os.path.isdir(self._directory_path):
            # It seems no lock has ever been queued to this device
            return None

        # Waiting for update token
        self.get_update_token()

        if not os.path.isfile(self._lock_file_path):
            _print("DEBUG: %s does not exist" % self._lock_file_path)
            # just update lock file, next check will get the info updated
            self._dequeue()
            self.release_update_token()
            return None

        lock_devices = _read_file(self._lock_file_path)
        if not lock_devices:
            _print("DEBUG: check_lock() - there is no lock for %s" % self._device_name)
            # just update lock file, next check will get the info updated
            self._dequeue()
            self.release_update_token()
            return None

        # _print("DEBUG: check_lock() - servers using %s are:" % self._device_name)
        # Check if locker was done by beaker task
        # if so, make sure task is still running
        for locked_host in lock_devices:
            m = self._lock_format_regex.match(locked_host)
            if not m:
                # invalid host format, delete it
                _print("WARN: %s is not valid lock host entry. Deleting it..." % locked_host)
                _delete_item_queue_file(self._lock_file_path, locked_host)
                continue

            # Check if lock was set by manual test run or beaker job
            if m.group(4) == "manual":
                current_timestamp = int(libsan.host.linux.time_stamp(in_seconds=True))
                timeout = int(m.group(3)) + (60 * 60)
                # timeout if locked manually for more than 1 hour
                if current_timestamp > timeout:
                    _print("INFO: manual lock '%s' timeout! Deleting lock..." % locked_host)
                    _delete_item_queue_file(self._lock_file_path, locked_host)
                    lock_devices.remove(locked_host)
                else:
                    _print("INFO: found manual lock, still has %s min left before timeout"
                           % ((timeout - current_timestamp) / 60))
                continue

            # Check if beaker task is still running
            t_status = beaker.get_task_status(m.group(4))
            if not t_status:
                # for some reason could not get beaker job status
                _print("WARN: Could not get status of beaker task %s" % m.group(4))
                # Check if it has been running for too long, in that case we remove the lock
                current_timestamp = int(libsan.host.linux.time_stamp(in_seconds=True))
                # 4hrs before timeout
                timeout = int(m.group(3)) + (4 * 60 * 60)
                # timeout if locked manually for more than 1 hour
                if current_timestamp > timeout:
                    _print("INFO: Task %s lock '%s' timeout! Deleting lock..." %
                           (m.group(4), locked_host))
                    _delete_item_queue_file(self._lock_file_path, locked_host)

            if t_status and t_status != "Running":
                # For example forgot to release the lock or server crashed...
                _print("INFO: Task for %s is on %s status. Not valid lock. "
                       "Deleting it..." % (locked_host, t_status))
                _delete_item_queue_file(self._lock_file_path, locked_host)
                # it will just be updated when we run check again

        # refresh queue, new info will get when we run check again
        self._dequeue()

        self.release_update_token()
        self.show_lock()
        return lock_devices

    def get_my_lock_info(self):
        """
        Check info for the my own lock
        """
        host = libsan.host.linux.hostname()
        self.check_lock()
        locked_list = self.check_lock()
        if locked_list:
            for locked_host in locked_list:
                m = self._lock_format_regex.match(locked_host)
                if m:
                    if host == m.group(1):
                        return locked_host
        return None

    def get_lock(self):
        """
        Wait until get the lock
        """
        host = libsan.host.linux.hostname()
        while True:
            task_id = beaker.get_task_id()
            # if it is a beaker task running
            if task_id:
                timeout = beaker.get_task_timeout(task_id)
                if timeout and timeout < 120:
                    _print("FAIL: Beaker task is about to time out, do not wait for lock")
                    _delete_item_queue_file(self._queue_file_path, host)
                    return None
            locked_list = self.check_lock()
            if locked_list:
                for locked_host in locked_list:
                    m = self._lock_format_regex.match(locked_host)
                    if m:
                        if host == m.group(1):
                            # we got the lock
                            return locked_host
            self.show_queue()
            self.show_lock()
            libsan.host.linux.sleep(60)

    def release_lock(self, lock_type, wait_time=120):
        """
        Release the lock
        """
        if not lock_type:
            _print("FAIL: release_lock() - requires lock_type parameter")
            return False

        host = libsan.host.linux.hostname()

        # Waiting for update token
        self.get_update_token()

        lock_devices = _read_file(self._lock_file_path)
        if not lock_devices:
            _print("INFO: release_lock() - Empty lock data")
            self.release_update_token()
            return True
        for locked_host in lock_devices:
            m = self._lock_format_regex.match(locked_host)
            if not m:
                # invalid host format, delete it
                _print("WARN: release_lock() - %s is not valid lock host entry. "
                       "Deleting it..." % locked_host)
                _delete_item_queue_file(self._lock_file_path, locked_host)
                continue
            if host == m.group(1):
                _print("INFO: Releasing lock %s" % locked_host)
                _delete_item_queue_file(self._lock_file_path, locked_host)

        self.release_update_token()
        if self._monitor_pid:
            libsan.host.linux.kill_pid(self._monitor_pid)
        # slepp 5mins to allow other servers to request lock
        _print("INFO: lock from %s is released. Waiting %s seconds to give chance "
               "to other servers" % (self._lock_file_path, wait_time))
        libsan.host.linux.sleep(wait_time)
        return True

    # def monitor_lock(self):
    #   """
    #   """
    #   host = linux.hostname()
    #   while True:
    #       locked_host = self.get_my_lock_info(wait_for_lock=False)
    #       if locked_host:
    #           m = self._lock_format_regex.match(locked_host)
    #           if m and m.group(1) == host:
    #               _print("Refreshing lock info...")
    #               _delete_item_queue_file(self._lock_file_path, locked_host)
    #               self._add_host(m.group(1), m.group(2))
    #       linux.sleep(5*60)

    #   _print("INFO: Stopping monitoring lock")
    #   return False

    def show_lock(self):
        """
        Show hosts with lock
        """
        _print("INFO: ### Showing NFS lock data #########")
        cmd = "cat %s " % self._lock_file_path
        ret, output = run(cmd, return_output=True, verbose=False)
        print(output)
        _print("INFO: ### End NFS lock data #########")
        return True

    #   ######### TEST ###############
    def _self_test(self):
        """
        Basic self test
        """
        # device_name = "self_test"
        self.mount_lock()
        _print("######## TEST 1 #########")
        self.get_update_token()
        self.release_update_token()
        _print("#PASS - TEST 1")
        _print("######## TEST 2 #########")
        self.request_lock("shared")
        _print("#TEST2: Requested shared lock")
        self.check_lock()
        _print("#TEST2: checked lock")
        self.show_queue()
        _print("#TEST2: Trying to get lock")
        self.get_lock()
        _print("#TEST2: Got lock")
        self.show_lock()
        _print("#TEST2: Trying to release lock")
        self.release_lock("shared")
        _print("#TEST2: Lock released")
        self.show_lock()
        _print("#TEST2: Released shared lock")
        _print("#PASS - TEST 2")
        _print("######## TEST 3 #########")
        self.show_queue()
        self.show_lock()
        _print("#PASS - TEST 3")
        self.umount_lock()

        # linux.umount(self._mount_point)
        # if not self.mount_lock():
        #   _print("FAIL: _self_test() - Could not mount NFS share")
        #   linux.umount(self._mount_point)
        #   return False

        # self.show_lock()

        # if not self.request_lock("shared"):
        #   _print("FAIL: _self_test() - Could not request lock")
        #   linux.umount(self._mount_point)
        #   return False
        # self.show_queue()

        # self.show_lock()

        # if not self._add_queue(host2, "shared"):
        #   _print("FAIL: _self_test() - Could not add %s to queue" % host2)
        #   linux.umount(self._mount_point)
        #   return False

        # self.show_lock()

        # if not self.check_lock():
        #   _print("INFO: _self_test() - No server pending on %s" % self._device_name)

        # if not self.check_lock():
        #   _print("FAIL: _self_test() - We expected to find a device waiting for lock")
        #   linux.umount(self._mount_point)
        #   return False

        # if not self.release_lock("shared"):
        #   _print("FAIL: Could not release lock")
        #   linux.umount(self._mount_point)
        #   return False

        # if not self.check_lock():
        #   _print("INFO: _self_test() - No server pending on %s" % self._device_name)
        # self.show_lock()

        # linux.umount(self._mount_point)
        return True
