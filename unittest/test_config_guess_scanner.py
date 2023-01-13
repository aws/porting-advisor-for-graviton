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
from src.advisor.scanners.config_guess_scanner import ConfigGuessScanner


class TestConfigGuessScanner(unittest.TestCase):
    def test_accepts_file(self):
        config_guess_scanner = ConfigGuessScanner()
        self.assertFalse(config_guess_scanner.accepts_file('test'))
        self.assertTrue(config_guess_scanner.accepts_file('config.guess'))

    def test_scan_file_object(self):
        config_guess_scanner = ConfigGuessScanner()
        report = Report('/root')
        io_object = io.StringIO('xxx')
        config_guess_scanner.scan_file_object(
            'config.guess', io_object, report)
        self.assertEqual(len(report.issues), 1)
        report = Report('/root')
        io_object = io.StringIO('aarch64:Linux')
        config_guess_scanner.scan_file_object(
            'config.guess', io_object, report)
        self.assertEqual(len(report.remarks), 1)
