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
from .issues.issue_types import ISSUE_TYPES
from .report import Report

class CsvIssueTypeCountByFileReport(Report):
    """Generates a CSV report with a 'issue type count by file' schema."""

    def __init__(self, root_directory, target_os='linux', issue_type_config=None):
        """Generates a CSV report with a 'issue type count by file' schema.

        issue_type_config (IssueTypeConfig): issue type filter configuration.
        """
        super().__init__(root_directory, target_os)
        self.issue_type_config = issue_type_config

    def write_items(self, output_file, items):
        issue_types = self.issue_type_config.filter_issue_types(ISSUE_TYPES)
        csv_writer = csv.writer(output_file)
        header = ['filename'] + [issue_type.display_name() for issue_type in issue_types]
        csv_writer.writerow(header)
        sorted_source_files = sorted(self.source_files)
        issue_type_totals_by_file = {}
        for source_file in sorted_source_files:
            issue_type_totals = {issue_type: 0 for issue_type in ISSUE_TYPES.values()}
            issue_type_totals_by_file[source_file] = issue_type_totals
        for item in items:
            issue_type_totals_by_file[item.filename][item.__class__] += 1
        for source_file in sorted_source_files:
            issue_type_totals = issue_type_totals_by_file[source_file]
            row = [source_file] + [issue_type_totals[issue_type] for issue_type in issue_types]
            csv_writer.writerow(row)
