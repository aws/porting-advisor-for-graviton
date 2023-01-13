import io
import unittest
from src.advisor.reports.issues.dependency_version_issue import DependencyVersionIssue
from src.advisor.reports.issues.unsupported_dependency_issue import UnsupportedDependencyIssue
from src.advisor.reports.remarks.dependency_version_remark import DependencyVersionRemark
from src.advisor.reports.remarks.special_instructions_remark import SpecialInstructionsRemark
from src.advisor.reports.report import Report
from src.advisor.scanners.java_scanner import JavaScanner


class TestJavaScaner(unittest.TestCase):
    def setUp(self) -> None:
        self.scanner = JavaScanner()
        self.report = Report('/root')

    def test_accepts_file(self):
        self.assertFalse(self.scanner.accepts_file('test.txt'))
        self.assertTrue(self.scanner.accepts_file('pom.xml'))

    def test_scan_file_object_with_unreported_dependency_finds_no_issues(self):
        io_object = io.StringIO('''<project>
  <artifactId>my-test1</artifactId>
  <version>1.0</version>
  
  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.8.2</version> 
    </dependency>
  </dependencies>
</project>''')
        self.scanner.scan_file_object('pom.xml', io_object, self.report)
        self.assertEqual(0, len(self.report.issues))
        self.assertEqual(0, len(self.report.remarks))
        self.assertEqual(0, len(self.report.errors))

    def test_scan_file_object_with_valid_versions_finds_no_issues(self):
        io_object = io.StringIO('''<project>
  <artifactId>my-test1</artifactId>
  <version>1.0</version>
  
  <dependencies>
    <dependency>
      <groupId>com.github.luben</groupId>
      <artifactId>zstd-jni</artifactId>
      <version>1.2.0</version>
    </dependency>
    <dependency>
      <groupId>org.xerial.snappy</groupId>
      <artifactId>snappy-java</artifactId>
      <version>1.1.8.4</version>
    </dependency>
  </dependencies>
</project>
        ''')
        self.scanner.scan_file_object('pom.xml', io_object, self.report)
        self.assertEqual(0, len(self.report.issues))

    def test_scan_file_object_with_invalid_version_finds_issues(self):
        io_object = io.StringIO('''<project>
  <artifactId>my-test1</artifactId>
  <version>1.0</version>
  
  <dependencies>
    <dependency>
      <groupId>com.github.luben</groupId>
      <artifactId>zstd-jni</artifactId>
      <version>1.1.0</version>
    </dependency>
    <dependency>
      <groupId>org.xerial.snappy</groupId>
      <artifactId>snappy-java</artifactId>
      <version>1.1.3</version>
    </dependency>
    <dependency>
      <groupId>org.lz4</groupId>
      <artifactId>lz4-java</artifactId>
      <version>1.4.0</version>
    </dependency>
  </dependencies>
</project>
        ''')
        self.scanner.scan_file_object('pom.xml', io_object, self.report)
        self.assertEqual(2, len(self.report.issues))
        self.assertIsInstance(self.report.issues[0], DependencyVersionIssue)
        self.assertIsInstance(self.report.issues[1], DependencyVersionIssue)

    def test_scan_file_object_with_library_with_manual_build_requirement_adds_warning(self):
        io_object = io.StringIO('''<project>
  <artifactId>my-test1</artifactId>
  <version>1.0</version>
  
  <dependencies>
    <dependency>
        <groupId>com.hadoop.gplcompression</groupId>
        <artifactId>hadoop-lzo</artifactId>
        <version>0.4.17</version>
        </dependency>
    </dependencies>
</project>
        ''')
        self.scanner.scan_file_object('pom.xml', io_object, self.report)
        self.assertEqual(1, len(self.report.remarks))
        self.assertIsInstance(self.report.remarks[0], SpecialInstructionsRemark)

    def test_scan_file_object_with_unsupported_library_finds_issue(self):
        io_object = io.StringIO('''<project>
  <artifactId>my-test1</artifactId>
  <version>1.0</version>
  
  <dependencies>
    <dependency>
        <groupId>org.fusesource.leveldbjni</groupId>
        <artifactId>leveldbjni-all</artifactId>
        <version>1.8</version>
    </dependency>
  </dependencies>
</project>
        ''')
        self.scanner.scan_file_object('pom.xml', io_object, self.report)
        self.assertEqual(1, len(self.report.issues))
        self.assertIsInstance(self.report.issues[0], UnsupportedDependencyIssue)

    def test_scan_file_object_without_version_specified_adds_remark(self):
        io_object = io.StringIO('''<project>
  <artifactId>my-test1</artifactId>
  <version>1.0</version>
  
  <dependencies>
    <dependency>
      <groupId>jffi</groupId>
      <artifactId>jffi</artifactId>
      <scope>compile</scope>
    </dependency>
  </dependencies>
</project>
        ''')
        self.scanner.scan_file_object('pom.xml', io_object, self.report)
        self.assertEqual(1, len(self.report.remarks))
        self.assertIsInstance(self.report.remarks[0], DependencyVersionRemark)
    
    def test_scan_file_object_with_version_in_property_node_adds_issue(self):
        io_object = io.StringIO(r'''<project>
  <artifactId>my-test1</artifactId>
  <version>1.0</version>
  <properties>
    <snappy.version>1.1.3</snappy.version>
  </properties>
  
  <dependencies>
    <dependency>
      <groupId>org.xerial.snappy</groupId>
      <artifactId>snappy-java</artifactId>
      <version>${snappy.version}</version>
    </dependency>
  </dependencies>
</project>
        ''')
        self.scanner.scan_file_object('pom.xml', io_object, self.report)
        self.assertEqual(1, len(self.report.issues))
        self.assertIsInstance(self.report.issues[0], DependencyVersionIssue)

    def test_scan_file_object_with_java_files_adds_language_version_remark(self):
        io_object = io.StringIO('System.out.println("Hello, World!");')
        self.scanner.scan_file_object('main.java', io_object, self.report)
        self.assertEqual(2, len(self.report.remarks))
        self.assertEqual(
            f'detected java code. min version 8 is required. version 11 or above is recommended. see https://github.com/aws/aws-graviton-getting-started/blob/main/java.md for more details.',
            self.report.remarks[0].description
        )
        self.assertEqual(
            f'detected java code. we recommend using Corretto. see https://aws.amazon.com/corretto/ for more details.',
            self.report.remarks[1].description
        )
