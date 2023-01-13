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

import csv
import io
import tempfile
import unittest
from src.advisor.reports.csv_report import CsvReport
from src.advisor.scanners.config_guess_scanner import ConfigGuessScanner
from src.advisor.scanners.source_scanner import SourceScanner


class TestCsvReport(unittest.TestCase):
    def test_output(self):
        config_guess_scanner = ConfigGuessScanner()
        source_scanner = SourceScanner()

        report = CsvReport('/root')
        report.add_source_file('test_negative.c')
        io_object = io.StringIO('__asm__("mov r0, r1")')
        source_scanner.scan_file_object(
            'test_negative.c', io_object, report)
        report.add_source_file('test_neutral.c')
        io_object = io.StringIO('#pragma simd foo')
        source_scanner.scan_file_object(
            'test_neutral.c', io_object, report)
        report.add_source_file('config.guess')
        io_object = io.StringIO('aarch64:Linux')
        config_guess_scanner.scan_file_object(
            'config.guess', io_object, report)
        self.assertEqual(len(report.issues), 2)
        self.assertEqual(len(report.remarks), 1)

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as ofp:
            report.write(ofp)
            fname = ofp.name
            ofp.close()

            with open(fname) as ifp:
                csv_reader = csv.DictReader(ifp)
                seen_issue1 = False
                seen_issue2 = False
                for row in csv_reader:
                    if 'test_negative.c' in row['filename']:
                        self.assertIn('InlineAsm', row['issue_type'])
                        seen_issue1 = True
                    elif 'test_neutral.c' in row['filename']:
                        self.assertIn('PragmaSimd', row['issue_type'])
                        seen_issue2 = True
                    else:
                        self.fail('Unexpected row in CSV output')
                self.assertTrue(seen_issue1)
                self.assertTrue(seen_issue2)
