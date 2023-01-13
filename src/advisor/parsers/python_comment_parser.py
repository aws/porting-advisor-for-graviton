from ..parsers.comment_parser import CommentParser


class PythonCommentParser(CommentParser):
    """Python comment parser."""

    def __init__(self):
        super(PythonCommentParser, self).__init__('#', '"""', '"""')
