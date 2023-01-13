import os
from os import path
from ..helpers.java.java_tool_invoker import JavaToolInvoker
from ..manifester.manifester import Manifester
from ..reports.issues.native_methods_issue import NativeMethodsIssue
from ..reports.report_item import ReportItem
from .language_scanner import LanguageScanner


class JavaScanner(LanguageScanner):
    """Scanner that checks Java files for potential porting issues."""

    def __init__(self) -> None:
        self.LANGUAGE_NAME = 'java'
        self._added_jar_remark = False
        super().__init__()

    def scan_file_object(self, filename, file_object, report):
        """Scans the provided file and adds issues, remarks, or errors as needed to the Report.

        Args:
            filename: The name of the file being checked.
            file_object: The file contents.
            report: The report being generated.
        """
        if self.has_source_extension(filename):
            self._add_java_language_remark(report)
            _, ext = os.path.splitext(filename)
            tool_invoker = JavaToolInvoker()
            is_jar_or_war = ext == '.jar' or ext == '.war'
            if is_jar_or_war and tool_invoker.can_run():
                result, message = tool_invoker.graviton_ready_assessor(filename)
                if (result == 3):
                    report.add_issue(NativeMethodsIssue(message, filename=filename))
            elif is_jar_or_war:
                self.add_jar_remark(report)

            return

        if path.basename(filename) in self.DEPENDENCY_FILES:
            manifester = Manifester()
            dependencies = manifester.get_dependencies(filename, file_object, report)
            self.add_library_remarks(dependencies, report)
    
    def _add_java_language_remark(self, report):
        """Adds the Java version and Corretto recommendations.

        Args:
            report: The report to add the remark to.
        """
        self.add_language_remarks(report)

    def add_jar_remark(self, report):
        if self._added_jar_remark == False:
            report.add_remark(ReportItem('java is not installed. we need java to scan jar files for native methods'))
            self._added_jar_remark = True
