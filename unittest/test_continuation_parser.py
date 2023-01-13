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
from src.advisor.parsers.continuation_parser import ContinuationParser


class TestOsFilter(unittest.TestCase):
    def test_parse_line(self):
        continuation_parser = ContinuationParser()
        line = continuation_parser.parse_line('just a line')
        self.assertEqual(line, 'just a line')
        line = continuation_parser.parse_line('')
        self.assertEqual(line, '')
        line = continuation_parser.parse_line('#define MACRO \\')
        self.assertIsNone(line)
        line = continuation_parser.parse_line('first line of macro \\')
        self.assertIsNone(line)
        line = continuation_parser.parse_line('second line of macro')
        self.assertEqual(line, '#define MACRO first line of macro second line of macro')
