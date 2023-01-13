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

import os
from ..reports.issues.config_guess_issue import ConfigGuessIssue
from ..reports.remarks.config_guess_remark import ConfigGuessRemark
from .scanner import Scanner


class ConfigGuessScanner(Scanner):
    """Scanner that scans config.guess files for aarch64 support."""

    def accepts_file(self, filename):
        return os.path.basename(filename) == 'config.guess'

    def scan_file_object(self, filename, file, report):
        for line in file:
            if 'aarch64:Linux' in line:
                report.add_remark(ConfigGuessRemark(filename=filename))
                break
        else:
            report.add_issue(ConfigGuessIssue(filename=filename))
