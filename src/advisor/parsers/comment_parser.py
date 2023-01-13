class CommentParser:
    """Comment parser base."""

    def __init__(self, one_line_token, multi_line_begin_token, multi_line_end_token):
        self._in_comment = False
        self._one_line_token = one_line_token
        self._multi_line_begin_token = multi_line_begin_token
        self._multi_line_end_token = multi_line_end_token
    
    def parse_line(self, line):
        """Parse comments in a source line

        Args:
            line (str): The line to parse.
        
        Returns:
            bool: Whether this line is a comment
        """
        if line.lstrip().startswith(self._one_line_token):
            return True
        if self._in_comment:
            if self._multi_line_end_token in line:
                self._in_comment = False
            return True
        else:
            if line.lstrip().startswith(self._multi_line_begin_token):
                templine = line[2:]
                if not self._multi_line_end_token in templine:
                    self._in_comment = True
                    return True
                elif templine.rstrip().endswith(self._multi_line_end_token):
                    return True
        return False