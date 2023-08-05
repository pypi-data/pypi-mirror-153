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

"""beaker.py: Module to manage beaker."""

__author__ = "Bruno Goncalves"
__copyright__ = "Copyright (c) 2016 Red Hat, Inc. All rights reserved."

import re  # regex
import os
import libsan.host.linux
from libsan.host.cmdline import run


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


def update_killtime(kill_time):
    """
    Change beaker watchdog kill time
    Parameter:
    \tkill_time     new kill time in hours
    Return:
    \tTrue
    or
    \tFalse
    """
    if not is_bkr_job():
        return False

    if not kill_time:
        kill_time = 1

    result_server = os.environ['RESULT_SERVER']
    jobid = os.environ['JOBID']
    test = os.environ['TEST']
    testid = os.environ['TESTID']

    host = libsan.host.linux.hostname()
    cmd = "rhts-test-checkin %s %s %s %s %s %s" % (result_server, host, jobid, test, kill_time, testid)
    ret, output = run(cmd, return_output=True, verbose=False)
    if ret != 0:
        _print("FAIL: Could not update beaker kill time")
        print(output)
        return False
    _print("INFO: beaker_update_killtime() - Watchdog timer successfully updated to %d hours" % kill_time)
    return True


def get_task_timeout(task_id):
    """
    Get how much time the task still has
    Parameter:
    \ttask_id:          Beaker Task ID
    Return:
    \tNone:             In case of some problem
    or
    \tint(value):       The remaining time in seconds
    """
    if not is_bkr_job():
        return None

    if task_id is None:
        _print("FAIL: beaker get_task_timeout() - requires task_id as parameter")
        return None

    cmd = "bkr watchdog-show %s" % task_id
    ret, output = run(cmd, return_output=True, verbose=False)
    if ret != 0:
        _print("FAIL: beaker get_task_timeout() - Could not get beaker kill time")
        print(output)
        return None

    output_regex = re.compile("%s: (\d+)" % task_id)
    m = output_regex.match(output)
    if m:
        return int(m.group(1))
    _print("FAIL: beaker get_task_timeout() - Could not parse output:")
    print(output)
    return None


def log_submit(log_file):
    """
    """
    if not is_bkr_job():
        return True

    if not log_file:
        _print("FAIL: log_submit() - requires log_file parameter")
        return False

    if not os.path.exists(log_file):
        _print("FAIL: log_submit() - file does not exist" % log_file)
        return False

    cmd = "rhts-submit-log -l \"%s\"" % log_file
    ret, output = run(cmd, return_output=True, verbose=False)
    if ret != 0:
        _print("FAIL: Could not upload log %s" % log_file)
        print(output)
        return False
    _print("INFO: log_submit() - %s uploaded successfully" % log_file)
    return True


def get_task_id():
    """
    Get current task id
    Parameter:
    \tNone
    Return:
    \ttask_id:          Beaker task ID
    or
    \tNone:             Some error occurred
    """
    if not is_bkr_job():
        return None
    return os.environ['TASKID']


def get_task_status(task_id):
    """
    Requires beaker-client package installed and configured
    """
    if not is_bkr_job():
        return None

    if not task_id:
        _print("FAIL: get_task_status() - requires task ID")
        return None

    cmd = "bkr job-results --prettyxml T:%s" % task_id
    ret, output = run(cmd, return_output=True, verbose=False)
    if ret != 0:
        _print("FAIL: get_task_status() - Could not get beaker task result for T:%s" % task_id)
        print(output)
        return None

    lines = output.split("\n")
    status_regex = re.compile("<task.*status=\"(\S+)\"")
    for line in lines:
        m = status_regex.match(line)
        if m:
            return m.group(1)
    return None


def is_bkr_job():
    """
    Checks if is beaker job
    """
    need_env = ["RESULT_SERVER", "JOBID", "TEST", "TESTID", "TASKID"]
    for var in need_env:
        if var not in os.environ:
            return False

    result_server = os.environ['RESULT_SERVER']
    jobid = os.environ['JOBID']
    test = os.environ['TEST']
    testid = os.environ['TESTID']

    if not result_server or not jobid or not test or not testid:
        return False

    return True
