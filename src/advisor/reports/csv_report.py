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

import csv
from .report import Report

class CsvReport(Report):
    """Generates a CSV report."""

    def write_items(self, output_file, items):
        csv_writer = csv.writer(output_file)
        header = ['filename', 'function', 'line', 'issue_type', 'description']
        csv_writer.writerow(header)
        for item in items:
            issue_type = item.__class__.display_name()
            row = [item.filename, item.function, item.lineno, issue_type, item.description]
            csv_writer.writerow(row)
