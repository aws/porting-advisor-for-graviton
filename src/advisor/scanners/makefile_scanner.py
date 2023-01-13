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
import re
from ..constants.arch_strings import AARCH64_ARCHS, NON_AARCH64_ARCHS
from ..constants.arch_specific_libs import ARCH_SPECIFIC_LIBS
from ..parsers.continuation_parser import ContinuationParser
from ..reports.issues.arch_specific_library_issue import ArchSpecificLibraryIssue
from ..reports.issues.build_command_issue import BuildCommandIssue
from ..reports.issues.define_other_arch_issue import DefineOtherArchIssue
from ..reports.issues.host_cpu_detection_issue import HostCpuDetectionIssue
from ..reports.issues.old_crt_issue import OldCrtIssue
from .scanner import Scanner


class MakefileScanner(Scanner):
    """Scanner that scans Makefiles."""

    MAKEFILE_NAMES = ['Makefile.in', 'Makefile.am']
    MAKEFILE_NAMES_CASE_INSENSITIVE = ['makefile', 'nmakefile', 'makefile.mk']

    ARCH_SPECIFIC_LIBS_RE_PROG = re.compile(r'-l(%s)' %
                                            '|'.join([(r'%s\b' % x) for x in ARCH_SPECIFIC_LIBS]))
    OLD_CRT_RE_PROG = re.compile(r'(libcmt[a-z]*\.lib)', re.IGNORECASE)
    UCRT_RE_PROG = re.compile(r'(libucrt[a-z]*\.lib)', re.IGNORECASE)
    OTHER_ARCH_CPU_LINE_RE_PROG = re.compile(r'\$\((?:CPU|PROCESSOR_ARCHITECTURE)\).*(%s)' %
                                  '|'.join(NON_AARCH64_ARCHS))
    AARCH64_CPU_LINE_RE_PROG = re.compile(r'\$\(VSCMD_ARG_TGT_ARCH\).*(%s)' %
                                  '|'.join(AARCH64_ARCHS))
    TARGET_RE_PROG = re.compile(r'^([a-zA-Z()$_0-9\./]+)\s*:')
    COMMAND_RE_PROG = re.compile(r'^\t(?:([a-zA-Z()$_0-9\./]+)|"([a-zA-Z()$_0-9\./ ]+)")(?:$|\s)')
    ASSIGNMENT_RE_PROG = re.compile(r'^([a-zA-Z()$_0-9]+)\s*=\s*(.*)$')
    D_OTHER_ARCH_RE_PROG = re.compile(r'[-/]D(%s)' %
                                      '|'.join(NON_AARCH64_ARCHS +
                                               [x.upper() for x in NON_AARCH64_ARCHS] + 
                                               [('_%s_' % x) for x in NON_AARCH64_ARCHS] + 
                                               [('_%s_' % x.upper()) for x in NON_AARCH64_ARCHS] +
                                               [('__%s__' % x) for x in NON_AARCH64_ARCHS] + 
                                               [('__%s__' % x.upper()) for x in NON_AARCH64_ARCHS]))
    D_AARCH64_RE_PROG = re.compile(r'[-/]D(%s)' %
                                   '|'.join(AARCH64_ARCHS +
                                            [x.upper() for x in AARCH64_ARCHS] +
                                            [('_%s_' % x) for x in AARCH64_ARCHS] +
                                            [('_%s_' % x.upper()) for x in AARCH64_ARCHS] +
                                            [('__%s__' % x) for x in AARCH64_ARCHS] +
                                            [('__%s__' % x.upper()) for x in AARCH64_ARCHS]))

    def accepts_file(self, filename):
        basename = os.path.basename(filename)
        return basename in MakefileScanner.MAKEFILE_NAMES or \
               basename.lower() in MakefileScanner.MAKEFILE_NAMES_CASE_INSENSITIVE

    def scan_file_object(self, filename, file, report):
        continuation_parser = ContinuationParser()
        old_crt_lib_name = None
        seen_ucrt = False
        other_arch_cpu_condition = None
        seen_aarch64_cpu_condition = False
        d_other_arch = None
        seen_d_aarch64 = False
        targets = set()
        commands = set()
        assignments = dict()
        continuation_line = None

        for lineno, line in enumerate(file, 1):
            line = continuation_parser.parse_line(line)

            if not line:
                continue

            match = MakefileScanner.ARCH_SPECIFIC_LIBS_RE_PROG.search(line)
            if match:
                lib_name = match.group(1)
                report.add_issue(ArchSpecificLibraryIssue(
                    filename, lineno + 1, lib_name))
            match = MakefileScanner.OLD_CRT_RE_PROG.search(line)
            if match:
                old_crt_lib_name = match.group(1)
            match = MakefileScanner.UCRT_RE_PROG.search(line)
            if match:
                seen_ucrt = True
            match = MakefileScanner.OTHER_ARCH_CPU_LINE_RE_PROG.search(line)
            if match:
                other_arch_cpu_condition = line
            match = MakefileScanner.AARCH64_CPU_LINE_RE_PROG.search(line)
            if match:
                seen_aarch64_cpu_condition = True
            match = MakefileScanner.TARGET_RE_PROG.search(line)
            if match:
                target = match.group(1)
                if target.startswith('./') or target.startswith('.\\'):
                    target = target[2:]
                targets.add(target)
            match = MakefileScanner.COMMAND_RE_PROG.search(line)
            if match:
                command = match.group(1)
                if not command:
                    command = match.group(2)
                if command.startswith('./') or command.startswith('.\\'):
                    command = command[2:]
                commands.add(command)
            match = MakefileScanner.ASSIGNMENT_RE_PROG.search(line)
            if match:
                assignments['$(%s)' % match.group(1)] = match.group(2)
            match = MakefileScanner.D_OTHER_ARCH_RE_PROG.search(line)
            if match:
                if not d_other_arch:
                    d_other_arch = match.group(1)
            match = MakefileScanner.D_AARCH64_RE_PROG.search(line)
            if match:
                seen_d_aarch64 = True

        if old_crt_lib_name and not seen_ucrt:
            report.add_issue(OldCrtIssue(
                    filename, lineno + 1, old_crt_lib_name))
        if other_arch_cpu_condition and not seen_aarch64_cpu_condition:
            report.add_issue(HostCpuDetectionIssue(filename, lineno + 1, other_arch_cpu_condition))
        build_commands = targets.intersection(commands)
        for command in build_commands:
            if command in assignments:
                command = assignments[command]
            report.add_issue(BuildCommandIssue(filename, lineno + 1, command))
        if d_other_arch and not seen_d_aarch64:
            report.add_issue(DefineOtherArchIssue(filename, lineno + 1, d_other_arch))
