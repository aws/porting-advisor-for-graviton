from .issue import Issue
from ..report_item import ReportItem


class NativeMethodsIssue(Issue):
    def __init__(self, native_methods, filename=None, lineno=None, item_type=ReportItem.NEGATIVE, function=None):
        description = f'JAR has native methods but no libraries found for aarch64/Linux. {native_methods}'
        super().__init__(description, filename, lineno, item_type, function)