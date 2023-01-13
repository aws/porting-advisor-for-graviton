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

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from os import getcwd, path
from .. import __version__
from .report import Report


class HtmlReport(Report):
    """Generates an HTML report from a template."""

    def write(self, output_file, report_errors=True, report_remarks=True, include_summary=True):
        """ Override write to report all items."""
        super().write(output_file, report_errors=report_errors,
                      report_remarks=report_remarks, include_summary=include_summary)

    def write_items(self, output_file, items):
        templates_folder = path.abspath(path.join(path.dirname(__file__), '..', 'templates'))

        env = Environment(
            loader=FileSystemLoader(templates_folder),
            autoescape=True
        )
        template = env.get_template('template.html')

        directory_name = path.normpath(self.root_directory)
        if (directory_name in ['.', './']):
            directory_name = path.basename(getcwd())
        
        base_name = path.basename(directory_name)
        report_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        rendered = template.render(
            root_directory=directory_name,
            root_directory_basename=base_name,
            report_date=report_date,
            tool_version=__version__,
            items=items)
        output_file.write(rendered)
