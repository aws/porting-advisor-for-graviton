import unittest
from src.advisor.parsers.ruby_gem_parser import RubyGemParser


class TestRubyGemParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = RubyGemParser()

    def test_gem_with_name_returns_name(self):
        expected = 'rails', None
        self.assertEqual(expected, self.parser.parse_line('"rails"'))
        self.assertEqual(expected, self.parser.parse_line("'rails'"))

    def test_gem_with_name_and_version_returns_name_and_version(self):
        expected = 'rails', '6.1.6.1'
        self.assertEqual(expected, self.parser.parse_line('"rails", "6.1.6.1"'))
        self.assertEqual(expected, self.parser.parse_line("'rails', '6.1.6.1'"))
    
    def test_gem_with_name_version_and_specifier_returns_name(self):
        expected = 'rails', '6.1.6.1'
        self.assertEqual(expected, self.parser.parse_line("'rails', '~> 6.1.6.1'"))
        self.assertEqual(expected, self.parser.parse_line('"rails", "~> 6.1.6.1"'))
        self.assertEqual(expected, self.parser.parse_line('"rails", "<= 6.1.6.1"'))
        self.assertEqual(expected, self.parser.parse_line('"rails", ">= 6.1.6.1"'))
        self.assertEqual(expected, self.parser.parse_line('"rails", ">= 6.1.6.1", "< 7.0.0"'))

    def test_gem_with_ternary_operator_returns_correct_value(self):
        expected = 'cucumber', '4.1'
        self.assertEqual(expected, self.parser.parse_line('"cucumber", RUBY_VERSION >= "2.5" ? "~> 5.1.2" : "~> 4.1"'))

    def test_gem_with_other_specifiers_returns_correct_value(self):
        expected = 'gssapi', None
        self.assertEqual(expected, self.parser.parse_line('"gssapi", group: :kerberos'))
        self.assertEqual(expected, self.parser.parse_line('"gssapi", require: false, platform: :mri'))
        self.assertEqual(expected, self.parser.parse_line('"gssapi", git: "https://github.com/gssapi"'))