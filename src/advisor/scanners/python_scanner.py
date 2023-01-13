from os import path
from ..helpers.python.python_version_checker import PythonVersionChecker
from ..manifester.manifester import Manifester
from .language_scanner import LanguageScanner


class PythonScanner(LanguageScanner):
    """Scanner that scans Python source files for potential porting issues."""

    def __init__(self) -> None:
        self.LANGUAGE_NAME = 'python'
        super().__init__()

    def scan_file_object(self, filename, file_object, report):
        """Scans the provided file and adds issues, remarks, or errors as needed to the Report.

        Args:
            filename: The name of the file being checked.
            file_object: The file contents.
            report: The report being generated.
        """
        if not self._added_language_version_remark and self.has_source_extension(filename):
            self._add_python_language_remark(report)
            return

        if path.basename(filename) in self.DEPENDENCY_FILES:
            manifester = Manifester()
            dependencies = manifester.get_dependencies(filename, file_object, report)
            self.add_library_remarks(dependencies, report)

    def _add_python_language_remark(self, report):
        """Adds the Python version recommendations.

        Args:
            report: The report to add the remark to.
        """
        self.INSTALLED_VERSION = PythonVersionChecker.get_python_version()
        installed_pip_version = PythonVersionChecker.get_pip_version()

        self.TOOLS_RULES['pip']['installedVersion'] = installed_pip_version
        
        self.add_language_remarks(report)
