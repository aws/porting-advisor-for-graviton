import os
import re
from ..manifester.manifester import Manifester
from .language_scanner import LanguageScanner


class GoScanner(LanguageScanner):
    """Scanner that checks Go files for potential porting issues."""

    def __init__(self) -> None:
        self.LANGUAGE_NAME = 'go'
        self.LANGUAGE_VERSION_RE = r'^go (?P<version>[\w\.]*)$'
        super().__init__()

    def scan_file_object(self, filename, file_object, report):
        """Scans the provided file and adds issues, remarks or errors as needed to the report.

        Args:
            filename: The name of the file being checked.
            file_object: The file contents.
            report: The report being generated.
        """
        if os.path.basename(filename) in self.DEPENDENCY_FILES:
            file_contents = file_object.read()
            go_match = re.findall(self.LANGUAGE_VERSION_RE, file_contents, re.MULTILINE)
            if go_match and go_match[0]:
                self.INSTALLED_VERSION = go_match[0]
                self.add_language_remarks(report)

            manifester = Manifester()
            dependencies = manifester.get_dependencies(filename, file_object, report)

            self.add_library_remarks(dependencies, report)
