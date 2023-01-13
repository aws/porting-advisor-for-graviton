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

import io
import unittest
from src.advisor.reports.report import Report
from src.advisor.scanners.asm_source_scanner import AsmSourceScanner


class TestAsmSourceScanner(unittest.TestCase):
    def test_accepts_file(self):
        asm_source_scanner = AsmSourceScanner()
        self.assertFalse(asm_source_scanner.accepts_file('test.c'))
        self.assertFalse(asm_source_scanner.accepts_file('tests'))
        self.assertTrue(asm_source_scanner.accepts_file('test.s'))
        self.assertTrue(asm_source_scanner.accepts_file('test.S'))

    def test_scan_file_object(self):
        asm_source_scanner = AsmSourceScanner()
        report = Report('/root')
        io_object = io.StringIO('__asm__("")')
        asm_source_scanner.scan_file_object('test.s', io_object, report)
        self.assertEqual(len(report.issues), 0)
        report = Report('/root')
        io_object = io.StringIO('__asm__("mov r0, r1")')
        asm_source_scanner.scan_file_object('test.s', io_object, report)
        self.assertEqual(len(report.issues), 1)
