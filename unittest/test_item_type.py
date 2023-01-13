"""
Copyright 2020 Arm Ltd.

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
from src.advisor.reports.issues.compiler_specific_issue import CompilerSpecificIssue
from src.advisor.reports.report_item import ReportItem


class TestItemType(unittest.TestCase):
    def test_compiler_specific_issue(self):
        issue = CompilerSpecificIssue('filename', 123, 'compiler', 'function')
        self.assertEqual(issue.item_type, ReportItem.NEUTRAL)
