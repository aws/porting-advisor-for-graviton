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
from src.advisor.reports.issues.asm_source_issue import AsmSourceIssue
from src.advisor.reports.issues.compiler_specific_issue import CompilerSpecificIssue
from src.advisor.reports.issues.cross_compile_issue import CrossCompileIssue
from src.advisor.reports.issues.inline_asm_issue import InlineAsmIssue
from src.advisor.reports.issues.issue_type_config import IssueTypeConfig
from src.advisor.reports.issues.issue_types import ISSUE_TYPES
from src.advisor.reports.issues.no_equivalent_issue import NoEquivalentIssue
from src.advisor.reports.issues.pragma_simd_issue import PragmaSimdIssue
from src.advisor.reports.issues.preprocessor_error_issue import PreprocessorErrorIssue


class TestIssueTypeConfig(unittest.TestCase):
    def test_none(self):
        def is_expected_filtered(issue_type):
            # Assumes DEFAULT_FILTER = '-CompilerSpecific,-CrossCompile,-NoEquivalent'
            return issubclass(issue_type, CompilerSpecificIssue) or \
                   issubclass(issue_type, CrossCompileIssue) or \
                   issubclass(issue_type, NoEquivalentIssue)

        expected_issue_types = [issue_type for issue_type in ISSUE_TYPES.values() if not is_expected_filtered(issue_type)]
        issue_type_config = IssueTypeConfig(None)
        actual_issue_types = issue_type_config.filter_issue_types(ISSUE_TYPES)
        self.assertEqual(set(expected_issue_types), set(actual_issue_types))
        expected_included_issue = PreprocessorErrorIssue('foo', 'bar', 'wibble')
        self.assertTrue(issue_type_config.include_issue_p(expected_included_issue))
        expected_excluded_issue = CompilerSpecificIssue('foo', 'bar', 'wibble')
        self.assertFalse(issue_type_config.include_issue_p(expected_excluded_issue))

    def test_explicit_list(self):
        expected_issue_types = [PreprocessorErrorIssue, AsmSourceIssue, InlineAsmIssue]
        issue_type_config = IssueTypeConfig('PreprocessorError,AsmSource,InlineAsm')
        actual_issue_types = issue_type_config.filter_issue_types(ISSUE_TYPES)
        self.assertEqual(expected_issue_types, actual_issue_types)
        expected_included_issue = PreprocessorErrorIssue('foo', 'bar', 'wibble')
        self.assertTrue(issue_type_config.include_issue_p(expected_included_issue))
        expected_excluded_issue = CompilerSpecificIssue('foo', 'bar', 'wibble')
        self.assertFalse(issue_type_config.include_issue_p(expected_excluded_issue))
        expected_excluded_issue = PragmaSimdIssue('foo', 'bar', 'wibble') # not in explicit list
        self.assertFalse(issue_type_config.include_issue_p(expected_excluded_issue))

    def test_include(self):
        def is_expected_filtered(issue_type):
            # Assumes DEFAULT_FILTER = '-CompilerSpecific,-CrossCompile,-NoEquivalent'
            return issubclass(issue_type, CrossCompileIssue) or \
                   issubclass(issue_type, NoEquivalentIssue)

        expected_issue_types = [issue_type for issue_type in ISSUE_TYPES.values() if not is_expected_filtered(issue_type)]
        issue_type_config = IssueTypeConfig('+CompilerSpecific')
        actual_issue_types = issue_type_config.filter_issue_types(ISSUE_TYPES)
        self.assertEqual(set(expected_issue_types), set(actual_issue_types))
        expected_included_issue = PreprocessorErrorIssue('foo', 'bar', 'wibble')
        self.assertTrue(issue_type_config.include_issue_p(expected_included_issue))
        expected_excluded_issue = NoEquivalentIssue('foo', 'bar', 'wibble')
        self.assertFalse(issue_type_config.include_issue_p(expected_excluded_issue))

    def test_exclude(self):
        def is_expected_filtered(issue_type):
            # Assumes DEFAULT_FILTER = '-CompilerSpecific,-CrossCompile,-NoEquivalent'
            return issubclass(issue_type, CompilerSpecificIssue) or \
                   issubclass(issue_type, CrossCompileIssue) or \
                   issubclass(issue_type, NoEquivalentIssue) or \
                   issubclass(issue_type, PreprocessorErrorIssue)

        expected_issue_types = [issue_type for issue_type in ISSUE_TYPES.values() if not is_expected_filtered(issue_type)]
        issue_type_config = IssueTypeConfig('-PreprocessorError')
        actual_issue_types = issue_type_config.filter_issue_types(ISSUE_TYPES)
        self.assertEqual(set(expected_issue_types), set(actual_issue_types))
        expected_included_issue = PragmaSimdIssue('foo', 'bar', 'wibble')
        self.assertTrue(issue_type_config.include_issue_p(expected_included_issue))
        expected_excluded_issue = PreprocessorErrorIssue('foo', 'bar', 'wibble')
        self.assertFalse(issue_type_config.include_issue_p(expected_excluded_issue))
