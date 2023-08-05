#!/usr/bin/python
# Copyright (C) 2017 Red Hat, Inc.
# iscsi_params.py is a part of python-stqe
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
#
# Author: Martin Hoyer   <mhoyer@redhat.com>

from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import random
import sys
import libsan.host.linux as linux
import libsan.host.fio as fio
import libsan.host.iscsi as iscsi
import libsan.host.lio as lio
import libsan.host.mp as mp
import libsan.host.scsi as scsi
from six.moves import range
from six.moves import zip

from stqe.host.LogChecker import check_all

t_iqn = 'iqn.2017-11.com.redhat:params-test'  # Target IQN.
parameters = ['HeaderDigest', 'MaxRecvDataSegmentLength', 'MaxXmitDataSegmentLength', 'FirstBurstLength',
              'MaxBurstLength', 'ImmediateData', 'InitialR2T']  # Parameters to be changed.

# Same parameters in /etc/iscsid.conf. Using escape characters as a workaround for bug in Augeas iscsid lens.
iscsid_params = ['node.conn\[0\].iscsi.HeaderDigest', 'node.conn\[0\].iscsi.MaxRecvDataSegmentLength',
                 'node.conn\[0\].iscsi.MaxXmitDataSegmentLength', 'node.session.iscsi.FirstBurstLength',
                 'node.session.iscsi.MaxBurstLength', 'node.session.iscsi.ImmediateData',
                 'node.session.iscsi.InitialR2T']


def generate_values():  # Generating random values from the pools for both target and initiator.
    tgt_values = []
    in_values = []

    # Pools for random choice.
    digest = ['None', 'None,CRC32C', 'CRC32C,None']  # Separate 'CRC32C' option to prevent 'CRC32C'+'None' situations
    byte = ["512", "1024", "2048", "4096", "8192", "16384", "32768", "65536", "131072", "262144", "524288", "1048576",
            "16777212"]
    yesno = ['Yes', 'No']
    crc = random.getrandbits(2)  # Generates 0-3
    if linux.dist_ver() > 7:
        if crc == 0:
            tgt_values.append('CRC32C')
            in_values.append('CRC32C')
        else:
            tgt_values.append(random.choice(digest))
            in_values.append(random.choice(digest))

    for _ in range(4):
        tgt_values.append(random.choice(byte))
        in_values.append(random.choice(byte))

    for _ in range(2):
        tgt_values.append(random.choice(yesno))
        in_values.append(random.choice(yesno))

    return tgt_values, in_values


def discovery_login():  # Discovering and logging into targets on localhost. There should be only one.
    iscsi.discovery_st('127.0.0.1', disc_db=True, ifaces='default')

    if not iscsi.node_login(portal='127.0.0.1', udev_wait_time=5):
        print('FAIL: Unable log into the target')
        return False

    return True


def do_io(device):  # fio - running randwrite until the 256M device is full, then verifying written data using CRC32C.
    if not fio.install_fio():
        print('FAIL: Unable to install fio')
        return False

    fio_params = {'bs': '4k', 'direct': 1, 'ioengine': 'libaio', 'iodepth': 16, 'verify': 'crc32c', 'verify_fatal': 1,
                  'do_verify': 1, 'rw': 'randwrite', 'runtime': 120}  # adding runtime cap of 2 minutes

    if not fio.fio_stress(device, verbose=True, **fio_params):
        print('FIO I/O failed')
        return False

    return True


def cleanup():
    if not (iscsi.clean_up() and lio.lio_clearconfig()):
        print("FAIL: Unable to clean-up iSCSI environment")
        return False

    return True


def main():
    print("INFO: Checking logs before iscsi_params test")
    if not check_all():
        print("WARN: Detected an error on LogChecker")

    parser = argparse.ArgumentParser()
    # noinspection PyTypeChecker
    parser.add_argument("--iterations", "-i", default=10, required=False, dest="iterations",
                        help="number of iterations", type=int)

    args = parser.parse_args()

    if not iscsi.install():
        return False

    if linux.dist_ver() < 8:
        parameters.remove("HeaderDigest")
        iscsid_params.remove("node.conn\[0\].iscsi.HeaderDigest")

    for _ in range(args.iterations):
        target_val, initiator_val = generate_values()
        tgt_params_values = dict(list(zip(parameters, target_val)))
        in_params_values = dict(list(zip(iscsid_params, initiator_val)))
        iscsi.clean_up()

        # Installing targetcli, clearing previous configuration, creating 256M local LIO target.
        if not lio.lio_setup_iscsi_target(lun_size='256M', tgt_iqn=t_iqn):
            return False

        # Setting parameter values with targetcli.
        for param in tgt_params_values:
            if not lio.lio_iscsi_target_set_parameter(tgt_iqn=t_iqn, tpg='tpg1', group='parameter', attr_name=param,
                                                      attr_value=tgt_params_values[param]):
                return False

        if not iscsi.set_iscsid_parameter(**in_params_values):  # Setting parameter values in /etc/iscsid.conf.
            return False

        if not discovery_login():
            return False

        # How to check params manually:
        # iscsiadm -m session -P2 | grep HeaderDigest | cut -d " " -f 2
        # cat /sys/class/iscsi_connection/connection*/header_digest
        # cat /sys/class/iscsi_session/session*/first_burst_len

        # Printing negotiated values.
        sid = iscsi.get_all_session_ids()
        if not sid:
            print("FAIL: Could not find session ID to use...")
            return False
        negotiated = iscsi.query_iscsi_session(sid[0])

        session_info_dict = {'HeaderDigest': 'header_digest', 'MaxRecvDataSegmentLength': 'max_recv',
                             'MaxXmitDataSegmentLength': 'max_xmit', 'FirstBurstLength': 'first_burst',
                             'MaxBurstLength': 'max_burst', 'ImmediateData': 'immediate_data',
                             'InitialR2T': 'initial_r2t'}

        count = 0
        for p in parameters:
            t_value = target_val[count]
            i_value = initiator_val[count]
            n_value = negotiated[session_info_dict[p]]
            n_expected = None
            print(p + ':')
            print('Target: %-11s| Initiator: %-11s| Negotiated: %-11s' % (t_value, i_value, n_value))
            print('______________________________________________________________\n')

            # Check if negotiated values are correct
            if p == 'HeaderDigest':
                if i_value.split(',')[0] == 'CRC32C':  # Initiator preference has priority.
                    n_expected = 'CRC32C'
                else:
                    n_expected = 'None'

                if (i_value == 'CRC32C,None') and (t_value == 'None'):
                    n_expected = 'None'

            elif p == 'MaxRecvDataSegmentLength':
                n_expected = i_value

            elif (p == 'MaxXmitDataSegmentLength') or (p == 'MaxBurstLength') or (p == 'FirstBurstLength'):
                if int(t_value) < int(i_value):
                    n_expected = t_value
                else:
                    n_expected = i_value

            elif p == 'ImmediateData':
                if (t_value == 'Yes') and (i_value == 'Yes'):
                    n_expected = 'Yes'
                else:
                    n_expected = 'No'

            elif p == 'InitialR2T':
                if (t_value == 'No') and (i_value == 'No'):
                    n_expected = 'No'
                else:
                    n_expected = 'Yes'

            if p == 'FirstBurstLength':
                # FirstBurstLength cannot be higher than MaxBurstLength
                if int(target_val[count + 1]) < int(initiator_val[count + 1]):
                    exp_max_burst = target_val[count + 1]
                else:
                    exp_max_burst = initiator_val[count + 1]

                if int(n_expected) > int(exp_max_burst):
                    n_expected = exp_max_burst

            if n_expected != n_value:
                print("FAIL: expected: %s, negotiated: %s" % (n_expected, n_value))
                return False

            count += 1

        # Choosing device to run IO on.
        test_dev = None
        if linux.is_service_running(mp.mp_service_name()):
            mpaths = mp.get_free_mpaths()
            if mpaths:
                test_dev = '/dev/mapper/' + list(mpaths.keys())[0]
            else:
                print("FAIL: multipathd is running but no free mpath devices found.")
                file = open('/etc/multipath.conf', 'r')
                print('/etc/multipath.conf:\n\n', file.read())
                return False
        else:
            dev = scsi.get_free_disks(filter_only={'model': 'params-test_lun'})
            if not dev:
                print("FAIL: Could not find device to use...")
                return False
            test_dev = '/dev/' + list(dev.keys())[0]

        if not do_io(test_dev):
            return False

        if not check_all():
            print("FAIL: Detected error on LogChecker")
            return False


if main() is False:
    cleanup()
    sys.exit(1)

if not cleanup():
    sys.exit(1)
