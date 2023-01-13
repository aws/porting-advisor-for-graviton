import io
import pkg_resources
import platform
import unittest
from src.advisor.reports.report import Report
from src.advisor.reports.report_item import ReportItem
from src.advisor.scanners.python_scanner import PythonScanner

class TestPythonScanner(unittest.TestCase):
    def setUp(self) -> None:
        self.scanner = PythonScanner()
        self.report = Report('/root')

    def test_accepts_file(self):
        self.assertFalse(self.scanner.accepts_file('test.txt'))
        self.assertTrue(self.scanner.accepts_file('requirements.txt'))

    def test_scan_file_object_with_unreported_dependency_finds_no_issues(self):
        io_object = io.StringIO('MyFakeDependency >= 1.2.3')
        self.scanner.scan_file_object('requirements.txt', io_object, self.report)
        self.assertEqual(0, len(self.report.issues))
        self.assertEqual(0, len(self.report.remarks))
        self.assertEqual(0, len(self.report.errors))

    def test_scan_file_object_with_valid_versions_finds_no_issues(self):
        io_object = io.StringIO('SciPy >= 1.7.2')
        self.scanner.scan_file_object('requirements.txt', io_object, self.report)
        self.assertEqual(0, len(self.report.issues))

    def test_scan_file_object_with_equals_valid_version_finds_no_issues(self):
        io_object = io.StringIO('SciPy = 1.7.2')
        self.scanner.scan_file_object('requirements.txt', io_object, self.report)
        self.assertEqual(0, len(self.report.issues))

    def test_scan_file_object_with_invalid_version_finds_issues(self):
        io_object = io.StringIO('SciPy >= 1.5.2')
        self.scanner.scan_file_object('requirements.txt', io_object, self.report)
        self.assertEqual(1, len(self.report.issues))
        self.assertEqual(ReportItem.NEGATIVE, self.report.issues[0].item_type)

    def test_scan_file_object_with_undefined_version_finds_remark(self):
        io_object = io.StringIO('SciPy')
        self.scanner.scan_file_object('requirements.txt', io_object, self.report)
        self.assertEqual(1, len(self.report.remarks))
        self.assertEqual(ReportItem.NEUTRAL, self.report.remarks[0].item_type)
    
    def test_scan_file_object_with_undefined_version_and_invalid_installed_version_finds_issues(self):
        io_object = io.StringIO('jinja2')
        self.scanner.LIBRARY_RULES = {'jinja2': { 'name': 'jinja2', 'minVersion': '100.2.3'}}
        self.scanner.scan_file_object('requirements.txt', io_object, self.report)
        self.assertEqual(1, len(self.report.issues))
        self.assertEqual(ReportItem.NEGATIVE, self.report.issues[0].item_type)
        
    def test_scan_file_object_with_undefined_version_and_valid_installed_version_finds_no_issues(self):
        io_object = io.StringIO('porting-advisor')
        self.scanner.LIBRARY_SPECIFIERS = {'porting-advisor': '1.4.1'}
        self.scanner.LIBRARY_RULES = {'porting-advisor': { 'name': 'porting-advisor', 'minVersion': '1.4.1'}}
        self.scanner.scan_file_object('requirements.txt', io_object, self.report)
        self.assertEqual(1, len(self.report.remarks))
        self.assertEqual(ReportItem.NEUTRAL, self.report.remarks[0].item_type)

    def test_scan_file_object_with_python_files_cause_language_version_remark(self):
        runtime_version = platform.python_version()
        pip_version = pkg_resources.get_distribution('pip').version
        io_object = io.StringIO('some python code')
        self.scanner.scan_file_object('main.py', io_object, self.report)
        self.assertEqual(2, len(self.report.remarks))
        self.assertEqual(
            f'detected python code. min version 3.7.5 is required. we detected that you have version {runtime_version}. see https://github.com/aws/aws-graviton-getting-started/blob/main/python.md for more details.',
            self.report.remarks[0].description)
        self.assertEqual(
            f'detected python code. if you need pip, version 19.3 or above is recommended. we detected that you have version {pip_version}.',
            self.report.remarks[1].description)
    
    def test_scan_file_object_with_non_python_files_dont_add_language_version_remark(self):
        io_object = io.StringIO('some random text')
        self.scanner.scan_file_object('main.java', io_object, self.report)
        self.assertEqual(0, len(self.report.remarks))

    def test_scan_file_object_is_case_insensitive(self):
        io_object = io.StringIO('numpy')
        self.scanner.scan_file_object('requirements.txt', io_object, self.report)
        self.assertEqual(1, len(self.report.remarks))
        self.assertEqual(
            'dependency library numpy is present. min version 1.19.0 is required.',
            self.report.remarks[0].description
        )