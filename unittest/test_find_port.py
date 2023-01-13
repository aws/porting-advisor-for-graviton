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
import unittest
from src.advisor.helpers.find_port import *


class TestFindPort(unittest.TestCase):
    def test_port_filenames(self):
        self.assertListEqual(port_filenames("filename"), [])
        self.assertListEqual(port_filenames("otherarch"),
                             ['arm', 'aarch64', 'arm64', 'neon', 'sve'])
        self.assertListEqual(port_filenames("source-otherarch.c"),
                             ['source-arm.c', 'source-aarch64.c',
                              'source-arm64.c', 'source-neon.c',
                              'source-sve.c'])

    def test_find_port_dir(self):
        self.assertEqual(find_port_dir('/foo/otherarch',
                                       ['/foo/otherarch', '/foo/aarch64']),
                         '/foo/aarch64')

    @unittest.skipIf(os.name == 'nt', 'Test fails in Windows')
    def test_find_port_file(self):
        self.assertEqual(find_port_file('/foo/source-otherarch.c',
                                        ['/foo/source-otherarch.c',
                                         '/foo/source-aarch64.c']),
                         '/foo/source-aarch64.c')
        self.assertEqual(find_port_file('/foo/otherarch/source.c',
                                        ['/foo/otherarch/source.c',
                                         '/foo/aarch64/source.c']),
                         '/foo/aarch64/source.c')

    @unittest.skipUnless(os.name == 'nt', 'test_find_port_file for Windows only')
    def test_find_port_file_windows(self):
        self.assertEqual(find_port_file('\\foo\\source-otherarch.c',
                                        ['\\foo\\source-otherarch.c',
                                         '\\foo\\source-aarch64.c']),
                         '\\foo\\source-aarch64.c')
        self.assertEqual(find_port_file('\\foo\\otherarch\\source.c',
                                        ['\\foo\\otherarch\\source.c',
                                         '\\foo\\aarch64\\source.c']),
                         '\\foo\\aarch64\\source.c')