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
import traceback
from ..reports.error import Error


class Scanner:
    VCS_SUBDIRECTORIES = ['.git', '.hg', '.svn', 'CVS']
    SOURCE_EXTENSION = []

    """List of (hidden) subdirectories used by version control systems."""
    def accepts_file(self, filename):
        """Overriden by subclasses to decide whether or not to accept a
        file.

        Args:
            filename (str): Filename under consideration.

        Returns:
            bool: True if the file with the given name is accepted by this
            scanner, else False.
        """
        return False

    def finalize_report(self, report):
        """Finalizes the report for this scanner.

        Args:
            report (Report): Report to finalize_report.
        """
        pass

    def has_scan_file_object(self):
        return hasattr(self, 'scan_file_object')

    def initialize_report(self, report):
        """Initialises the report for this scanner, which may include
        initializing scanner-specific fields in the Report.

        Args:
            report (Report): Report to initialize_report.
        """
        pass

    def scan_file(self, filename, report):
        """Scans the file with the given name for potential porting issues.

        Args:
            filename (str): Name of the file to scan.
            report (Report): Report to add issues to.
        """
        try:
            report.add_source_file(filename)
            self.scan_filename(filename, report)
            if self.has_scan_file_object():
                with open(filename, errors='ignore') as f:
                    try:
                        self.scan_file_object(filename, f, report)
                    except KeyboardInterrupt:
                        raise
                    except:
                        report.add_error(Error(description=str(traceback.format_exc()),
                                               filename=filename))
        except KeyboardInterrupt:
            raise
        except:
            report.add_error(Error(description=str(traceback.format_exc()),
                                   filename=filename))

    def scan_filename(self, filename, report):
        """Overridden by subclasses to scan for potential porting issues based
        on the name of the file.

        Args:
            filename (str): Name of the file to scan.
            report (Report): Report to add issues to.
        """
        pass

    def scan_tree(self, root, report, progress_callback=None):
        """Scans the filesysem tree starting at root for potential porting issues.

        Args:
            root (str): The root of the filesystem tree to scan.
            report (Report): Report to add issues to.
            progress_callback (function): Optional callback called with file names.
        """
        for dirName, _, fileList in os.walk(root):
            for fname in fileList:
                path = os.path.join(dirName, fname)
                if not Scanner._is_vcs_directory(path) and self.accepts_file(path):
                    if progress_callback:
                        progress_callback(path)
                    self.scan_file(path, report)

    @staticmethod
    def _is_vcs_directory(path):
        """Returns:
            bool: True if the path contains a version control directory (e.g. .git), else False.
        """
        return any([('/%s/' % x) in path for x in Scanner.VCS_SUBDIRECTORIES])
