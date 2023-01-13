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

import unittest
from src.advisor.filters.target_os_filter import TargetOsFilter
from src.advisor.reports.issues.config_guess_issue import ConfigGuessIssue
from src.advisor.reports.issues.inline_asm_issue import InlineAsmIssue
from src.advisor.reports.issues.old_crt_issue import OldCrtIssue
from src.advisor.reports.report import Report


class TestTargetOsFilter(unittest.TestCase):
    def test_finalize(self):
        report = Report('/root', target_os='linux')
        target_os_filter = TargetOsFilter()
        target_os_filter.initialize_report(report)
        report.add_source_file('test.c')
        report.add_issue(ConfigGuessIssue('test.c'))
        report.add_source_file('test.c')
        report.add_issue(InlineAsmIssue('test-aarch64.c', 123))
        target_os_filter.finalize_report(report)
        self.assertEqual(len(report.issues), 2)

        report = Report('/root', target_os='windows')
        target_os_filter = TargetOsFilter()
        target_os_filter.initialize_report(report)
        report.add_source_file('test.c')
        report.add_issue(ConfigGuessIssue('test.c'))
        report.add_source_file('test.c')
        report.add_issue(InlineAsmIssue('test-aarch64.c', 123))
        target_os_filter.finalize_report(report)
        self.assertEqual(len(report.issues), 1)

        report = Report('/root', target_os='all')
        target_os_filter = TargetOsFilter()
        target_os_filter.initialize_report(report)
        report.add_source_file('test.c')
        report.add_issue(ConfigGuessIssue('test.c'))
        report.add_source_file('test.c')
        report.add_issue(InlineAsmIssue('test-aarch64.c', 123))
        target_os_filter.finalize_report(report)
        self.assertEqual(len(report.issues), 2)

        report = Report('/root', target_os='linux')
        target_os_filter = TargetOsFilter()
        target_os_filter.initialize_report(report)
        report.add_source_file('test.c')
        report.add_issue(OldCrtIssue('test.c', 123, 'libcmt.lib'))
        report.add_source_file('test.c')
        report.add_issue(InlineAsmIssue('test-aarch64.c', 123))
        target_os_filter.finalize_report(report)
        self.assertEqual(len(report.issues), 1)

        report = Report('/root', target_os='windows')
        target_os_filter = TargetOsFilter()
        target_os_filter.initialize_report(report)
        report.add_source_file('test.c')
        report.add_issue(OldCrtIssue('test.c', 123, 'libcmt.lib'))
        report.add_source_file('test.c')
        report.add_issue(InlineAsmIssue('test-aarch64.c', 123))
        target_os_filter.finalize_report(report)
        self.assertEqual(len(report.issues), 2)

        report = Report('/root', target_os='all')
        target_os_filter = TargetOsFilter()
        target_os_filter.initialize_report(report)
        report.add_source_file('test.c')
        report.add_issue(OldCrtIssue('test.c', 123, 'libcmt.lib'))
        report.add_source_file('test.c')
        report.add_issue(InlineAsmIssue('test-aarch64.c', 123))
        target_os_filter.finalize_report(report)
        self.assertEqual(len(report.issues), 2)
