import re


class PythonRequirementsParser:
    """This parser looks for libraries in a Python requirements.txt file to identify
        library and required version."""
    
    SPECIFIER_RE = re.compile('(?P<name>[\w-]*)\s*(?P<comparer>[!<>=]*)\s*(?P<version>[\w\.]*)')

    def parse_line(self, line):
        """Parses a library line in a requirements.txt file

        Args:
            line (str): a line in a valid format. e.g. "SciPy>=1.7.2" or "SciPy"

        Returns:
            str, str, str: dependency name, version, comparer symbol
        """
        matches = PythonRequirementsParser.SPECIFIER_RE.search(line)
        return matches.group('name'), matches.group('version'), matches.group('comparer')