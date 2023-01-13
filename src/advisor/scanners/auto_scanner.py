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

from .scanner import Scanner


class AutoScanner(Scanner):
    """Scanner that automatically scans a file using one of a set of scanners,
    based on which scanner accepts the file."""

    def __init__(self, scanners):
        super().__init__()
        self.scanners = scanners

    def accepts_file(self, path):
        for scanner in self.scanners:
            if scanner.accepts_file(path):
                return True
        return False

    def scan_file(self, path, report):
        for scanner in self.scanners:
            if scanner.accepts_file(path):
                scanner.scan_file(path, report)
