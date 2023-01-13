"""
Copyright 2018 Arm Ltd.

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
from src.advisor.scanners.makefile_scanner import MakefileScanner


class TestMakefileScanner(unittest.TestCase):
    def test_accepts_file(self):
        makefile_scanner = MakefileScanner()
        self.assertFalse(makefile_scanner.accepts_file('test'))
        self.assertTrue(makefile_scanner.accepts_file('Makefile'))
        self.assertTrue(makefile_scanner.accepts_file('makefile'))
        self.assertTrue(makefile_scanner.accepts_file('MAKEFILE'))
        self.assertTrue(makefile_scanner.accepts_file('Makefile.in'))
        self.assertTrue(makefile_scanner.accepts_file('Makefile.am'))
        self.assertTrue(makefile_scanner.accepts_file('NMakefile'))
        self.assertTrue(makefile_scanner.accepts_file('nmakefile'))
        self.assertTrue(makefile_scanner.accepts_file('NMAKEFILE'))
        self.assertTrue(makefile_scanner.accepts_file('makefile.mk'))
        self.assertTrue(makefile_scanner.accepts_file('Makefile.mk'))
        self.assertTrue(makefile_scanner.accepts_file('MAKEFILE.MK'))

    def test_scan_file_object(self):
        makefile_scanner = MakefileScanner()
        report = Report('/root')
        io_object = io.StringIO('xxx')
        makefile_scanner.scan_file_object(
            'Makefile', io_object, report)
        self.assertEqual(len(report.issues), 0)


    def test_arch_specific_libs_re(self):
        match = MakefileScanner.ARCH_SPECIFIC_LIBS_RE_PROG.search('LIBS=-lfoo')
        self.assertIsNone(match)
        match = MakefileScanner.ARCH_SPECIFIC_LIBS_RE_PROG.search('LIBS=-lotherarch')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "otherarch")

    def test_arch_specific_libs(self):
        makefile_scanner = MakefileScanner()
        report = Report('/root')
        io_object = io.StringIO('-lotherarch')
        makefile_scanner.scan_file_object(
            'Makefile', io_object, report)
        self.assertEqual(len(report.issues), 1)

    def test_old_crt_re(self):
        match = MakefileScanner.OLD_CRT_RE_PROG.search('LIBS=libfoo.lib')
        self.assertIsNone(match)
        match = MakefileScanner.OLD_CRT_RE_PROG.search('LIBS=libcmt.lib')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "libcmt.lib")
        match = MakefileScanner.OLD_CRT_RE_PROG.search('LIBS=libcmtd.lib')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "libcmtd.lib") 

    def test_ucrt_re(self):
        match = MakefileScanner.UCRT_RE_PROG.search('LIBS=libfoo.lib')
        self.assertIsNone(match)
        match = MakefileScanner.UCRT_RE_PROG.search('LIBS=libucrt.lib')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "libucrt.lib")
        match = MakefileScanner.UCRT_RE_PROG.search('LIBS=libucrtd.lib')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "libucrtd.lib") 

    def test_old_crt(self):
        makefile_scanner = MakefileScanner()

        report = Report('/root')
        io_object = io.StringIO('LIBS=libcmt.lib')
        makefile_scanner.scan_file_object(
            'Makefile', io_object, report)
        self.assertEqual(len(report.issues), 1)

        report = Report('/root')
        io_object = io.StringIO('!IF $(OLD_CRT)\nLIBS=libcmt.lib\n!ELSE\nLIBS=libucrt.lib\n!ENDIF')
        makefile_scanner.scan_file_object(
            'Makefile', io_object, report)
        self.assertEqual(len(report.issues), 0)

    def test_other_arch_cpu_line_re(self):
        match = MakefileScanner.OTHER_ARCH_CPU_LINE_RE_PROG.search('!IF "$(CPU)" == "aarch64"')
        self.assertIsNone(match)
        match = MakefileScanner.OTHER_ARCH_CPU_LINE_RE_PROG.search('!IF "$(CPU)" == "otherarch"')
        self.assertIsNotNone(match)

    def test_aarch64_cpu_line_re(self):
        match = MakefileScanner.AARCH64_CPU_LINE_RE_PROG.search('!IF "$(CPU)" == "otherarch"')
        self.assertIsNone(match)
        match = MakefileScanner.AARCH64_CPU_LINE_RE_PROG.search('!IF "$(VSCMD_ARG_TGT_ARCH)" == "aarch64"')
        self.assertIsNotNone(match)

    def test_other_arch_cpu_line(self):
        makefile_scanner = MakefileScanner()

        report = Report('/root')
        io_object = io.StringIO('!IF "$(CPU)" == "otherarch"')
        makefile_scanner.scan_file_object(
            'Makefile', io_object, report)
        self.assertEqual(len(report.issues), 1)

        report = Report('/root')
        io_object = io.StringIO('!IF "$(VSCMD_ARG_TGT_ARCH)" == "arm"\nTARGET_ARCH=aarch64\n!ELIF "$(CPU)" == "otherarch"\nTARGET_ARCH=otherarch\n!ENDIF')
        makefile_scanner.scan_file_object(
            'Makefile', io_object, report)
        self.assertEqual(len(report.issues), 0)

    def test_target_re(self):
        match = MakefileScanner.TARGET_RE_PROG.search('\tsomecommand')
        self.assertIsNone(match)
        match = MakefileScanner.TARGET_RE_PROG.search('#a comment')
        self.assertIsNone(match)
        match = MakefileScanner.TARGET_RE_PROG.search('target:')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), 'target')
        match = MakefileScanner.TARGET_RE_PROG.search('$(TARGET):')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '$(TARGET)')

    def test_command_re(self):
        match = MakefileScanner.COMMAND_RE_PROG.search('#a comment')
        self.assertIsNone(match)
        match = MakefileScanner.COMMAND_RE_PROG.search('target:')
        self.assertIsNone(match)
        match = MakefileScanner.COMMAND_RE_PROG.search('$(TARGET):')
        self.assertIsNone(match)
        match = MakefileScanner.COMMAND_RE_PROG.search('\tsomecommand')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), 'somecommand')
        match = MakefileScanner.COMMAND_RE_PROG.search('\t"somecommand"')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(2), 'somecommand')
        match = MakefileScanner.COMMAND_RE_PROG.search('\tsomecommand arg')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), 'somecommand')
        match = MakefileScanner.COMMAND_RE_PROG.search('\t"somecommand" arg')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(2), 'somecommand')
        match = MakefileScanner.COMMAND_RE_PROG.search('\t"word1 word2" arg')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(2), 'word1 word2')
        match = MakefileScanner.COMMAND_RE_PROG.search('\t$(TARGET)')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '$(TARGET)')
        match = MakefileScanner.COMMAND_RE_PROG.search('\t$(TARGET) arg')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '$(TARGET)')
        match = MakefileScanner.COMMAND_RE_PROG.search('\t"$(TARGET)" arg')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(2), '$(TARGET)')
        match = MakefileScanner.COMMAND_RE_PROG.search('\t./target.exe arg')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), './target.exe')

    def test_target_command(self):
        makefile_scanner = MakefileScanner()

        report = Report('/root')
        io_object = io.StringIO('target.exe: target.c\n\tcl target.c /Fe:target.exe\n\nfoobar.h: target.exe\n\t./target.exe >foobar.h')
        makefile_scanner.scan_file_object(
            'Makefile', io_object, report)
        self.assertEqual(len(report.issues), 1)

        report = Report('/root')
        io_object = io.StringIO('$(TARGET): target.c\n\tcl target.c /Fe:target.exe\n\nfoobar.h: $(TARGET)\n\t$(TARGET) >foobar.h')
        makefile_scanner.scan_file_object(
            'Makefile', io_object, report)
        self.assertEqual(len(report.issues), 1)

    def test_assignment_re(self):
        match = MakefileScanner.ASSIGNMENT_RE_PROG.search('# foo')
        self.assertIsNone(match)
        match = MakefileScanner.ASSIGNMENT_RE_PROG.search('A=B')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), 'A')
        self.assertEqual(match.group(2), 'B')

    def test_target_command_with_assignment(self):
        makefile_scanner = MakefileScanner()

        report = Report('/root')
        io_object = io.StringIO('TARGET=target.exe\n\n$(TARGET): target.c\n\tcl target.c /Fe:target.exe\n\nfoobar.h: $(TARGET)\n\t$(TARGET) >foobar.h')
        makefile_scanner.scan_file_object(
            'Makefile', io_object, report)
        self.assertEqual(len(report.issues), 1)
        issue = report.issues[0]
        self.assertEqual(issue.target, 'target.exe')

    def test_d_other_arch_re(self):
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('/Dfoo')
        self.assertIsNone(match)
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('/Dotherarch')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), 'otherarch')
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('/D_otherarch_')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '_otherarch_')
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('/D__otherarch__')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '__otherarch__')
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('/Daarch64')
        self.assertIsNone(match)
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('/D_aarch64_')
        self.assertIsNone(match)
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('/D__aarch64__')
        self.assertIsNone(match)
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('-Dfoo')
        self.assertIsNone(match)
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('-Dotherarch')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), 'otherarch')
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('-D_otherarch_')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '_otherarch_')
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('-D__otherarch__')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '__otherarch__')
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('-Daarch64')
        self.assertIsNone(match)
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('-D_aarch64_')
        self.assertIsNone(match)
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('-D__aarch64__')
        self.assertIsNone(match)

    def test_d_aarch64_re(self):
        match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search('/Dfoo')
        self.assertIsNone(match)
        match = MakefileScanner.D_AARCH64_RE_PROG.search('/Daarch64')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), 'aarch64')
        match = MakefileScanner.D_AARCH64_RE_PROG.search('/D_aarch64_')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '_aarch64_')
        match = MakefileScanner.D_AARCH64_RE_PROG.search('/D__aarch64__')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '__aarch64__')
        match = MakefileScanner.D_AARCH64_RE_PROG.search('/Dotherarch')
        self.assertIsNone(match)
        match = MakefileScanner.D_AARCH64_RE_PROG.search('/D_otherarch_')
        self.assertIsNone(match)
        match = MakefileScanner.D_AARCH64_RE_PROG.search('/D__otherarch__')
        self.assertIsNone(match)
        match = MakefileScanner.D_AARCH64_RE_PROG.search('-Dfoo')
        self.assertIsNone(match)
        match = MakefileScanner.D_AARCH64_RE_PROG.search('-Daarch64')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), 'aarch64')
        match = MakefileScanner.D_AARCH64_RE_PROG.search('-D_aarch64_')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '_aarch64_')
        match = MakefileScanner.D_AARCH64_RE_PROG.search('-D__aarch64__')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '__aarch64__')
        match = MakefileScanner.D_AARCH64_RE_PROG.search('-Dotherarch')
        self.assertIsNone(match)
        match = MakefileScanner.D_AARCH64_RE_PROG.search('-D_otherarch_')
        self.assertIsNone(match)
        match = MakefileScanner.D_AARCH64_RE_PROG.search('-D__otherarch__')
        self.assertIsNone(match)

    def test_define_other_arch(self):
        makefile_scanner = MakefileScanner()

        report = Report('/root')
        io_object = io.StringIO('CFLAGS=/D__otherarch__')
        makefile_scanner.scan_file_object(
            'Makefile', io_object, report)
        self.assertEqual(len(report.issues), 1)

        report = Report('/root')
        io_object = io.StringIO('!IF "$(VSCMD_ARG_TGT_ARCH)" == "arm"\nCFLAGS=/D__arm__\n!ELIF "$(CPU)" == "otherarch"\nCFLAGS=/D__otherarch__\n!ENDIF')
        makefile_scanner.scan_file_object(
            'Makefile', io_object, report)
        self.assertEqual(len(report.issues), 0)

    def test_continuation(self):
        makefile_scanner = MakefileScanner()
        report = Report('/root')
        # Should be treated as a single line and only one issue reported.
        io_object = io.StringIO('LIBS=-lotherarch\\\n-lotherarch')
        makefile_scanner.scan_file_object(
            'Makefile', io_object, report)
        self.assertEqual(len(report.issues), 1)
