from __future__ import absolute_import, division, print_function, unicode_literals

# Copyright (C) 2019 Red Hat, Inc.
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

"""stratis.py: Module with test specific method for Stratis."""

from stqe.host.fmf_tools import get_env_args
from stqe.host.persistent_vars import read_var


def get_stratis_args(stratis_object):
    """
    Returns dict of arguments passed from FMF env vars
    :return: dict
    """
    arguments = dict(stratis_object.arguments)
    # Stratis does not use kwargs, only positional ones. SO we need to add them here manually.
    positional_args = ["pool_name", "blockdevs", "current", "new", "fs_name", "origin_name", "snapshot_name",
                       "new_name", "key_desc", "keyfile_path", "cmd", "clevis", "thumbprint", "tang_url", "trust_url",
                       "binding_method"]
    return get_env_args(list(arguments) + list(positional_args),
                        read_var("FILE_NAMES"),
                        {})
