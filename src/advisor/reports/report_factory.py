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

from .csv_report import CsvReport
from .csv_issue_type_count_by_file_report import CsvIssueTypeCountByFileReport
from .dependencies_report import DependencyReport
from .json_report import JsonReport
from .html_report import HtmlReport
from .text_report import TextReport
from enum import Enum

class ReportOutputFormat(Enum):
    AUTO = 'auto'
    CSV_ISSUE_TYPE_COUNT_BY_FILE = 'csv_issue_type_count_by_file'
    CSV = 'csv'
    JSON = 'json'
    HTML = 'html'
    TEXT = 'text'
    DEPENDENCIES = 'dependencies'
    DEFAULT = AUTO

class ReportFactory:
    """ Factory class for report output formats. """

    _OUTPUT_FORMAT_FOR_EXTENSION = {
        'json': ReportOutputFormat.JSON,
        'html': ReportOutputFormat.HTML,
        'htm' : ReportOutputFormat.HTML,
        'txt' : ReportOutputFormat.TEXT,
        'csv' : ReportOutputFormat.CSV
    }
    """ Dictionary mapping file extension to output format.

        Used to decide the output format from the output file name when the
        report output format is 'auto'. """

    def output_format_for_extension(self, extension):
        """ Choose an output format based on the given file name extension. """
        return ReportFactory._OUTPUT_FORMAT_FOR_EXTENSION.get(extension.lower(), None)

    def createReport(self, root_directory, target_os='linux', issue_type_config=None, output_format=ReportOutputFormat.TEXT):
        match output_format:
            case ReportOutputFormat.TEXT:
                report = TextReport(root_directory, target_os=target_os)
            case ReportOutputFormat.HTML:
                report = HtmlReport(root_directory, target_os=target_os)
            case ReportOutputFormat.CSV:
                report = CsvReport(root_directory, target_os=target_os)
            case ReportOutputFormat.CSV_ISSUE_TYPE_COUNT_BY_FILE:
                report = CsvIssueTypeCountByFileReport(root_directory, target_os=target_os, issue_type_config=issue_type_config)
            case ReportOutputFormat.JSON:
                report = JsonReport(root_directory, target_os=target_os, issue_type_config=issue_type_config)
            case ReportOutputFormat.DEPENDENCIES:
                report = DependencyReport(root_directory)
            case _:
                raise ValueError(output_format)
        return report
