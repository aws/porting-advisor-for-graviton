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
import re
from ..reports.issues.asm_source_issue import AsmSourceIssue
from .scanner import Scanner


class AsmSourceScanner(Scanner):
    """Scanner that looks for assembly source files."""

    ASM_SOURCE_EXTENSIONS = ['.s']

    INSTRUCTION_RE_PROG = re.compile('%[re][a-z]+|r[0-9],|^[a-z][ \t]+[0-9]')
    """Some assembly source files don't actually contain any architecture
    specific instructions. This is designed to match common
    instruction syntaxes."""

    def accepts_file(self, filename):
        _, ext = os.path.splitext(filename)
        return ext.lower() in AsmSourceScanner.ASM_SOURCE_EXTENSIONS

    def scan_file_object(self, filename, file, report):
        for line in file:
            if AsmSourceScanner.INSTRUCTION_RE_PROG.search(line):
                report.add_issue(AsmSourceIssue(filename))
                break
