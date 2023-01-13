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

import json
from .report import Report

class JsonReport(Report):
    """Generates a JSON report."""

    def __init__(self, root_directory, target_os='linux', issue_type_config=None):
        """Generates a JSON report.

        issue_type_config (IssueTypeConfig): issue type filter configuration.
        """
        super().__init__(root_directory, target_os)
        self.issue_types = issue_type_config.config_string if issue_type_config else None

    def write_items(self, output_file, items):
        # munge 'self' fields so it can be serialized
        self.source_dirs = list(self.source_dirs)
        self.issues = [i.__class__.__name__ + ': ' + str(i) for i in self.issues]
        self.errors = [i.__class__.__name__ + ': ' + str(i) for i in self.errors]
        self.remarks = [i.__class__.__name__ + ': ' + str(i) for i in self.remarks]
        print(json.dumps(self.__dict__, sort_keys=True, indent=4), file=output_file)
