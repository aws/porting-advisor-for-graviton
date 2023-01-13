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

from ..reports.issues.other_issues import OtherIssues
from ..scanners.scanner import Scanner


class OtherIssuesFilter(Scanner):
    """Abbreviates long lists of similar issues."""

    MAX_ISSUES_PER_FILE = 10

    def finalize_report(self, report):
        issues_per_file = {}
        new_issues = []
        for issue in report.issues:
            if issue.filename:
                if not issue.filename in issues_per_file:
                    issues_per_file[issue.filename] = 0
                if issues_per_file[issue.filename] < OtherIssuesFilter.MAX_ISSUES_PER_FILE:
                    new_issues.append(issue)
                issues_per_file[issue.filename] += 1
            else:
                new_issues.append(issue)
        for filename in issues_per_file:
            if issues_per_file[filename] > OtherIssuesFilter.MAX_ISSUES_PER_FILE:
                new_issues.append(OtherIssues(
                    filename, issues_per_file[filename]))
        report.issues = new_issues
