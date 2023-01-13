import io
import unittest
from src.advisor.reports.remarks.language_version_remark import LanguageVersionRemark
from src.advisor.reports.report import Report
from src.advisor.reports.report_item import ReportItem
from src.advisor.scanners.go_scanner import GoScanner


class TestGoScanner(unittest.TestCase):
    def setUp(self) -> None:
        self.scanner = GoScanner()
        self.report = Report('/root')

    def test_accepts_file(self):
        self.assertTrue(self.scanner.accepts_file('go.mod'))
        self.assertTrue(self.scanner.accepts_file('main.go'))

    def test_scan_file_object_with_unreported_dependency_finds_no_issues(self):
        io_object = io.StringIO('''module sample/graviton-invalid

go 1.18

require (
	github.com/emicklei/go-restful/v3 v3.8.0
)''')
        self.scanner.scan_file_object('go.mod', io_object, self.report)
        self.assertEqual(0, len(self.report.issues))
        self.assertEqual(1, len(self.report.remarks))
        self.assertEqual(0, len(self.report.errors))
    
    def test_scan_file_object_with_valid_version_finds_no_issues(self):
        io_object = io.StringIO('''module sample/graviton-invalid

go 1.18

require (
	github.com/golang/snappy v0.0.2
)''')
        self.scanner.scan_file_object('go.mod', io_object, self.report)
        self.assertEqual(0, len(self.report.issues))
        self.assertEqual(1, len(self.report.remarks))
        self.assertEqual(0, len(self.report.errors))
    
    def test_scan_file_object_with_invalid_version_adds_issue(self):
        io_object = io.StringIO('''module sample/graviton-invalid

go 1.18

require (
	github.com/golang/snappy v0.0.1
)''')
        self.scanner.scan_file_object('go.mod', io_object, self.report)
        self.assertEqual(1, len(self.report.issues))
        self.assertEqual(1, len(self.report.remarks))
        self.assertEqual(0, len(self.report.errors))
    
    def test_scan_file_object_with_go_mod_file_with_invalid_version_adds_language_version_issue(self):
        io_object = io.StringIO('''module sample/graviton-invalid

go 1.15
''')
        self.scanner.scan_file_object('go.mod', io_object, self.report)
        self.assertEqual(1, len(self.report.remarks))
        self.assertEqual(ReportItem.NEGATIVE, self.report.remarks[0].item_type)
        self.assertIsInstance(self.report.remarks[0], LanguageVersionRemark)
        self.assertEqual('detected go code. min version 1.16 is required. version 1.18 or above is recommended. we detected that you have version 1.15. see https://github.com/aws/aws-graviton-getting-started/blob/main/golang.md for more details.', self.report.remarks[0].description)

    def test_scan_file_object_with_go_mod_file_with_min_version_adds_language_version_remark(self):
        io_object = io.StringIO('''module sample/graviton-invalid

go 1.16
''')
        self.scanner.scan_file_object('go.mod', io_object, self.report)
        self.assertEqual(1, len(self.report.remarks))
        self.assertEqual(ReportItem.POSITIVE, self.report.remarks[0].item_type)
        self.assertEqual('detected go code. min version 1.16 is required. version 1.18 or above is recommended. we detected that you have version 1.16. see https://github.com/aws/aws-graviton-getting-started/blob/main/golang.md for more details.', self.report.remarks[0].description)
    
    def test_scan_file_object_with_go_mod_file_with_recommended_version_adds_language_version_remark(self):
        io_object = io.StringIO('''module sample/graviton-invalid

go 1.18
''')
        self.scanner.scan_file_object('go.mod', io_object, self.report)
        self.assertEqual(1, len(self.report.remarks))
        self.assertEqual(ReportItem.POSITIVE, self.report.remarks[0].item_type)
        self.assertEqual('detected go code. min version 1.16 is required. version 1.18 or above is recommended. we detected that you have version 1.18. see https://github.com/aws/aws-graviton-getting-started/blob/main/golang.md for more details.', self.report.remarks[0].description)
