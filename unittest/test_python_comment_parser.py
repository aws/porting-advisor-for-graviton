from src.advisor.parsers.python_comment_parser import PythonCommentParser
import unittest


class TestPythonCommentParser(unittest.TestCase):
    def test_parse_line(self):
        comment_parser = PythonCommentParser()
        self.assertFalse(comment_parser.parse_line('is not a comment'))
        self.assertTrue(comment_parser.parse_line('# single line comment'))
        self.assertFalse(comment_parser.parse_line('is not a comment'))
        self.assertTrue(comment_parser.parse_line('""" start of multi line comment'))
        self.assertTrue(comment_parser.parse_line(' middle of multi line comment'))
        self.assertTrue(comment_parser.parse_line('end of multi line comment """'))
        self.assertFalse(comment_parser.parse_line('is not a comment'))
        self.assertTrue(comment_parser.parse_line('""" single line comment """'))
        self.assertFalse(comment_parser.parse_line('is not a comment'))
        self.assertFalse(comment_parser.parse_line('comment in """ middle of """ line'))
