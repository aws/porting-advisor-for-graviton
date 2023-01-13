"""
Copyright 2017 Arm Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

SPDX-License-Identifier: Apache-2.0
"""

import os
import re
from ..constants.arch_strings import AARCH64_ARCHS, NON_AARCH64_ARCHS


def port_filenames(filename):
    """Given a source filename returns a list of possible source filenames for
    the aarch64 port equivalent.

    Args:
        filename (str): The filename to return the possible port filenames for.

    Returns:
        list: A list of possible source filenames for the aarch64 port
        equivalent of filename.
    """
    # Split on non-word characters. 'A_B_C' becomes ['A', 'B', 'C'].
    parts = re.split(r'(\W+)', filename)
    ret = []
    for i, part in enumerate(parts):
        if part in NON_AARCH64_ARCHS:
            for arm_arch in AARCH64_ARCHS:
                filename = ''.join(parts[:i]) + \
                    arm_arch + ''.join(parts[(i + 1):])
                ret.append(filename)
        elif part in AARCH64_ARCHS:
            ret.append(filename)
    return ret


def find_port_dir(dirname, other_dirs):
    """Given a directory path dir searches other_dirs for a directory that
    may be an aarch64 port of dir.

    Args:
        dirname (str): The directory to find the port for.
        other_dirs (list): The list of directories to search through for the
        port.

    Returns:
        str: A directory that may be an aarch64 port of dir, or None.

    Examples:
        >>> find_port_dir('/work/app/source/otherarch',
                          ['/work/app/source/common',
                           '/work/app/source/aarch64'])
        '/work/app/source/aarch64'
    """
    parts = dirname.split(os.sep)
    for i, last_part in enumerate(parts):
        filenames = port_filenames(last_part)
        for port_filename in filenames:
            port_path = os.sep.join(parts[:i] + [port_filename])
            if port_path in other_dirs:
                return port_path
    return None


def find_port_file(filename, other_files, other_files_dirs=None):
    """Given a filename file searches other_files for a file that may
    be an aarch64 port of file.

    Args:
        file (str): The file to find the port for.
        other_files (list): The list of files to search through for the port.
        other_files_dirs (set, optional): The set of directories containing
        the files in other_files.

    Returns:
        str: A file name that may be an aarch64 port of file, or Nine.

    Examples:
        >>> find_port_file('/work/app/source/kernel-otherarch.c',
                           ['/work/app/source/common.c',
                            '/work/app/source/kernel-aarch64.c'],
                           ['/work/app/source'])
        '/work/app/source/kernel-aarch64.c'
    """
    head, tail = os.path.split(filename)
    filenames = port_filenames(tail)
    for port_filename in filenames:
        port_path = os.path.join(head, port_filename)
        if port_path in other_files:
            return port_path
    if not other_files_dirs:
        other_files_dirs = set()
        for file in other_files:
            other_files_dirs.add(os.path.dirname(file))
    port_dir = find_port_dir(head, other_files_dirs)
    if port_dir:
        return os.path.join(port_dir, tail)
    return None

def is_aarch64_specific_file_name(filename):
    parts = re.split(r'(\W+)', filename)
    for part in parts:
        if part in AARCH64_ARCHS:
            return True
    return False
