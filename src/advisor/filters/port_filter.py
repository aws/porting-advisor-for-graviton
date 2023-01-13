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

from ..helpers.find_port import find_port_file
from ..reports.issues.no_equivalent_issue import NoEquivalentIssue
from ..reports.remarks.ported_source_files_remark import PortedSourceFilesRemark
from ..scanners.scanner import Scanner


class PortFilter(Scanner):
    """Filters out issues (e.g. inline assembly) that occur in source files
    for which a likely aarch64 port exists."""

    def finalize_report(self, report):
        ported_source_files = set()
        for filename in report.source_files:
            port_file = find_port_file(
                filename, report.source_files, report.source_dirs)
            if port_file:
                ported_source_files.add(filename)
        if ported_source_files:
            report.add_remark(PortedSourceFilesRemark(
                len(ported_source_files)))
        report.issues = [issue for issue in report.issues
                         if not (issue.filename and issue.filename in ported_source_files) or \
                             isinstance(issue, NoEquivalentIssue)]
