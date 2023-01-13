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

from .report import Report

class TextReport(Report):
    """Generates a text report."""

    def write(self, output_file, report_errors=True, report_remarks=True, include_summary=True):
        """ Override write to report all items."""
        super().write(output_file, report_errors=report_errors,
                      report_remarks=report_remarks, include_summary=include_summary)
