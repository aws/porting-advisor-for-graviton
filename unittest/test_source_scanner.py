"""
Copyright 2017-2019 Arm Ltd.

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
from src.advisor.filters.port_filter import PortFilter
from src.advisor.reports.remarks.ported_inline_asm_remark import PortedInlineAsmRemark
from src.advisor.reports.report import Report
from src.advisor.reports.report_item import ReportItem
from src.advisor.scanners.source_scanner import SourceScanner


class TestSourceScanner(unittest.TestCase):
    def test_accepts_file(self):
        source_scanner = SourceScanner()
        self.assertFalse(source_scanner.accepts_file('test'))
        self.assertTrue(source_scanner.accepts_file('test.c'))
        self.assertTrue(source_scanner.accepts_file('test.cc'))
        self.assertTrue(source_scanner.accepts_file('test.CC'))
        self.assertTrue(source_scanner.accepts_file('test.f90'))
        self.assertTrue(source_scanner.accepts_file('test.F'))

    def test_scan_file_object(self):
        source_scanner = SourceScanner()

        report = Report('/root')
        io_object = io.StringIO('xxx')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        self.assertEqual(len(report.issues), 0)

        report = Report('/root')
        io_object = io.StringIO('__asm__("")')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        self.assertEqual(len(report.issues), 0)

        report = Report('/root')
        io_object = io.StringIO('__asm__("mov r0, r1")')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        self.assertEqual(len(report.issues), 1)

        report = Report('/root')
        io_object = io.StringIO('_otherarch_intrinsic_xyz(123)')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        self.assertEqual(len(report.issues), 1)

        report = Report('/root')
        io_object = io.StringIO('#pragma simd foo')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        self.assertEqual(len(report.issues), 1)
        self.assertEqual(report.issues[0].item_type, ReportItem.NEUTRAL)

    def test_comments_are_ignored(self):
        source_scanner = SourceScanner()

        report = Report('/root')
        io_object = io.StringIO('// __asm__("mov r0, r1")')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        self.assertEqual(len(report.issues), 0)

        report = Report('/root')
        io_object = io.StringIO('/*\n__asm__("mov r0, r1")\n*/')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        self.assertEqual(len(report.issues), 0)

    def test_function_name(self):
        source_scanner = SourceScanner()

        report = Report('/root')
        io_object = io.StringIO('void func(void) {\n__asm__("mov r0, r1");\n}')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        self.assertEqual(len(report.issues), 1)
        self.assertEqual(report.issues[0].function, 'func')

    def test_macro_name(self):
        source_scanner = SourceScanner()

        report = Report('/root')
        io_object = io.StringIO('#define MACRO __asm__("mov r0, r1")')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        self.assertEqual(len(report.issues), 1)
        self.assertEqual(report.issues[0].function, 'MACRO')

    def test_equivalent_inline_asm_file(self):
        source_scanner = SourceScanner()
        port_filter = PortFilter()

        report = Report('/root')
        port_filter.initialize_report(report)
        source_scanner.initialize_report(report)
        io_object = io.StringIO('__asm__("mov r0, r1")')
        report.add_source_file('otherarch.c')
        source_scanner.scan_file_object(
            'otherarch.c', io_object, report)
        io_object = io.StringIO('__asm__("mov r0, r1")')
        report.add_source_file('aarch64.c')
        source_scanner.scan_file_object(
            'aarch64.c', io_object, report)
        source_scanner.finalize_report(report)
        port_filter.finalize_report(report)
        self.assertEqual(len(report.issues), 0)
        found_ported_remark = False
        for remark in report.remarks:
            if isinstance(remark, PortedInlineAsmRemark):
                found_ported_remark = True
                break
        self.assertTrue(found_ported_remark)

    def test_no_equivalent_inline_asm_file(self):
        source_scanner = SourceScanner()
        port_filter = PortFilter()

        report = Report('/root')
        port_filter.initialize_report(report)
        source_scanner.initialize_report(report)
        io_object = io.StringIO('__asm__("mov r0, r1")')
        report.add_source_file('otherarch.c')
        source_scanner.scan_file_object(
            'otherarch.c', io_object, report)
        io_object = io.StringIO('foo')
        report.add_source_file('aarch64.c')
        source_scanner.scan_file_object(
            'aarch64.c', io_object, report)
        source_scanner.finalize_report(report)
        port_filter.finalize_report(report)
        self.assertEqual(len(report.issues), 1)

    def test_equivalent_intrinsic_file(self):
        source_scanner = SourceScanner()
        port_filter = PortFilter()

        report = Report('/root')
        port_filter.initialize_report(report)
        source_scanner.initialize_report(report)
        io_object = io.StringIO('_otherarch_intrinsic_xyz(123)')
        report.add_source_file('otherarch.c')
        source_scanner.scan_file_object(
            'otherarch.c', io_object, report)
        io_object = io.StringIO('_arm_intrinsic(123)')
        report.add_source_file('aarch64.c')
        source_scanner.scan_file_object(
            'aarch64.c', io_object, report)
        source_scanner.finalize_report(report)
        port_filter.finalize_report(report)
        self.assertEqual(len(report.issues), 0)

    def test_no_equivalent_intrinsic_file(self):
        source_scanner = SourceScanner()
        port_filter = PortFilter()

        report = Report('/root')
        port_filter.initialize_report(report)
        source_scanner.initialize_report(report)
        io_object = io.StringIO('_otherarch_intrinsic_xyz(123)')
        report.add_source_file('otherarch.c')
        source_scanner.scan_file_object(
            'otherarch.c', io_object, report)
        io_object = io.StringIO('foo')
        report.add_source_file('aarch64.c')
        source_scanner.scan_file_object(
            'aarch64.c', io_object, report)
        source_scanner.finalize_report(report)
        port_filter.finalize_report(report)
        self.assertEqual(len(report.issues), 1)

    def test_no_equivalent_inline_asm_single_file(self):
        source_scanner = SourceScanner()

        report = Report('/root')
        source_scanner.initialize_report(report)
        io_object = io.StringIO('__asm__("mov r0, r1"')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        source_scanner.finalize_report(report)
        self.assertEqual(len(report.issues), 2)

    def test_equivalent_inline_asm_function_outline(self):
        source_scanner = SourceScanner()

        report = Report('/root')
        source_scanner.initialize_report(report)
        io_object = io.StringIO('#if defined(__otherarch__)\nvoid func() {\n__asm__("mov r0, r1");\n}\n#elif defined(__aarch64__)\nvoid func() {\n__asm__("mov r0, r1");\n}\n#endif')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        source_scanner.finalize_report(report)
        self.assertEqual(len(report.issues), 0)

    def test_equivalent_inline_asm_function_inline(self):
        source_scanner = SourceScanner()

        report = Report('/root')
        source_scanner.initialize_report(report)
        io_object = io.StringIO('void func() {\n#if defined(__otherarch__)\n__asm__("mov r0, r1");\n#elif defined(__aarch64__)\n__asm__("mov r0, r1");\n#endif\n}')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        source_scanner.finalize_report(report)
        self.assertEqual(len(report.issues), 0)

    def test_no_equivalent_inline_asm_function_outline(self):
        source_scanner = SourceScanner()

        report = Report('/root')
        source_scanner.initialize_report(report)
        io_object = io.StringIO('#if defined(__otherarch__)\nvoid func() {\n__asm__("mov r0, r1");\n}\n#elif defined(__aarch64__)\nvoid func() {\nfoo\n}\n#endif')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        source_scanner.finalize_report(report)
        self.assertEqual(len(report.issues), 1)

    def test_no_equivalent_inline_asm_function_inline(self):
        source_scanner = SourceScanner()

        report = Report('/root')
        source_scanner.initialize_report(report)
        io_object = io.StringIO('void func() {\n#if defined(__otherarch__)\n__asm__("mov r0, r1");\n#elif defined(__aarch64__)\nfoo\n#endif\n}')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        source_scanner.finalize_report(report)
        self.assertEqual(len(report.issues), 1)

    def test_equivalent_intrinsic_function_outline(self):
        source_scanner = SourceScanner()

        report = Report('/root')
        source_scanner.initialize_report(report)
        io_object = io.StringIO('#if defined(__otherarch__)\nvoid func() {\n_otherarch_intrinsic_xyz(123);\n}\n#elif defined(__aarch64__)\nvoid func() {\n_arm_intrinsic(123);\n}\n#endif')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        source_scanner.finalize_report(report)
        self.assertEqual(len(report.issues), 0)

    def test_equivalent_intrinsic_function_inline(self):
        source_scanner = SourceScanner()

        report = Report('/root')
        source_scanner.initialize_report(report)
        io_object = io.StringIO('void func() {\n#if defined(__otherarch__)\n_otherarch_intrinsic_xyz(123);\n#elif defined(__aarch64__)\n_arm_intrinsic(123);\n#endif\n}')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        source_scanner.finalize_report(report)
        self.assertEqual(len(report.issues), 0)

    def test_no_equivalent_intrinsic_function_outline(self):
        source_scanner = SourceScanner()

        report = Report('/root')
        source_scanner.initialize_report(report)
        io_object = io.StringIO('#if defined(__otherarch__)\nvoid func() {\n_otherarch_intrinsic_xyz(123);\n}\n#elif defined(__aarch64__)\nvoid func() {\nfoo\n}\n#endif')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        source_scanner.finalize_report(report)
        self.assertEqual(len(report.issues), 1)

    def test_no_equivalent_intrinsic_function_inline(self):
        source_scanner = SourceScanner()

        report = Report('/root')
        source_scanner.initialize_report(report)
        io_object = io.StringIO('void func() {\n#if defined(__otherarch__)\n_otherarch_intrinsic_xyz(123));\n#elif defined(__aarch64__)\nfoo\n#endif\n}')
        source_scanner.scan_file_object(
            'test.c', io_object, report)
        source_scanner.finalize_report(report)
        self.assertEqual(len(report.issues), 1)
