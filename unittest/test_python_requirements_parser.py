import unittest
from src.advisor.parsers.python_requirements_parser import PythonRequirementsParser


class TestPythonRequirementsParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = PythonRequirementsParser()

    def test_parse_line_returns_name_version_and_comparer(self):
        expected = 'SciPy', '1.7.2', '>='
        self.assertEqual(expected, self.parser.parse_line('SciPy>=1.7.2'))
        self.assertEqual(expected, self.parser.parse_line('SciPy >= 1.7.2'))
    
    def test_parse_line_returns_name(self):
        expected = 'SciPy', '', ''
        self.assertEqual(expected, self.parser.parse_line('SciPy'))

    def test_parse_line_ignores_comments(self):
        expected = 'SciPy', '1.7.2', '>='
        self.assertEqual(expected, self.parser.parse_line('SciPy>=1.7.2 # this is a comment'))
        self.assertEqual(expected, self.parser.parse_line('SciPy >= 1.7.2 # this is a comment'))