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

from stqe.host.persistent_vars import write_file, read_env
import random


def range_key(lens):
    # return ''.join(random.sample(string.ascii_letters + string.digits, 100))
    keep_valid_codes = ""
    for i in range(lens):
        random_num = str(random.randint(0, 9))
        random_lower_alf = chr(random.randint(97, 122))
        random_upper_alf = chr(random.randint(65, 90))
        random_char = random.choice(
            [random_num, random_lower_alf, random_upper_alf])[0]
        keep_valid_codes += random_char
    return keep_valid_codes


def general_key(keyfile, lens=64, key="", ):
    if not key:
        key = range_key(lens)
    write_file(keyfile, key)
    return True


if __name__ == "__main__":
    keyfile = read_env('fmf_keyfile')
    lens = read_env('fmf_lens')
    try:
        key = read_env('fmf_key')
    except KeyError:
        key = ''
    general_key(keyfile, lens, key)
