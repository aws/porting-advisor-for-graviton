"""
Copyright 2017-2018 Arm Ltd.

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

import os
from .remarks.files_scanned_remark import FilesScannedRemark
from .remarks.no_issues_found_remark import NoIssuesFoundRemark
from .report_item import ReportItem

class Report:
    def __init__(self, root_directory, target_os='linux'):
        self.issues = []
        self.errors = []
        self.remarks = []
        self.root_directory = root_directory
        self.source_files = []
        self.source_dirs = set()
        self.target_os = target_os
        self.open_text_mode = 'w'
        self.send_filename = False
        self.self_process = False

    def add_source_file(self, source_file):
        self.source_files.append(source_file)
        self.source_dirs.add(os.path.dirname(source_file))

    def add_issue(self, item):
        self.issues.append(item)

    def add_remark(self, item):
        self.remarks.append(item)

    def add_error(self, error):
        self.errors.append(error)

    def write(self, output_file, report_errors=False, report_remarks=False, include_summary=False):
        items = {}
        for item_type in ReportItem.TYPES:
            items[item_type] = []
        all_items = []
        if report_remarks:
            all_items += self.remarks
        all_items += self.issues
        if report_errors:
            all_items += self.errors
        for item in all_items:
            items[item.item_type].append(item)
        if include_summary:
            items[ReportItem.SUMMARY].append(
                FilesScannedRemark(len(self.source_files)))
            if not items[ReportItem.NEGATIVE] and not items[ReportItem.NEUTRAL] and report_remarks:
                items[ReportItem.POSITIVE].append(NoIssuesFoundRemark())
        sorted_items = []
        for item_type in ReportItem.TYPES:
            sorted_items += sorted(items[item_type], key=lambda item: (
                (item.filename if item.filename else '') + ':' + item.description))
        self.write_items(output_file, sorted_items)

    def write_items(self, output_file, items):
        for item in items:
            print(item, file=output_file)
