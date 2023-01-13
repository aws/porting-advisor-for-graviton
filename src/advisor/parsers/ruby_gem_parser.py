import re
from ..helpers.version_comparer import VersionComparer

class RubyGemParser:
    """This parser looks for libraries gems declared on the Gemfile file to identify
        library and required version."""
    
    SEMVER_RE = re.compile('(\d+\.*)+')
    TERNARY_RE = re.compile('.+ \? (?P<then>.+) : (?P<else>.+)')

    def parse_line(self, line):
        """Parses a gem declaration on the Gemfile file

        Args:
            line (str): a line in a valid format. e.g. "rails', '~> 6.1.6.1"

        Returns:
            str, str: dependency name, version
        """
        line = line.replace('\'', '"')
        sections = line.split(', ')

        if len(sections) > 0:
            name = sections[0].replace('"', '')
        
        version = ''
        ternary_versions = self._parse_ternary_expression(line)
        if (ternary_versions):
            version = self._parse_version_range(ternary_versions)
        else:
            version = self._parse_version_range(sections[1:])
        
        return name, version
    
    def _parse_version_range(self, versions: list[str]):
        """Cycle through a list of versions and find the lowest one"""
        lowest_version = None
        for version in versions:
            match = re.search(self.SEMVER_RE, version)
            if match:
                this_version = match.group(0)
                if VersionComparer.is_valid(this_version):
                    if not lowest_version or VersionComparer.compare(lowest_version, this_version) == 1:
                        lowest_version = this_version
        
        return lowest_version
    
    def _parse_ternary_expression(self, line: str):
        """Receives a ternary expression and returns a list consisting of the THEN and ELSE statements"""
        match = re.search(self.TERNARY_RE, line)
        if match:
            return [match.group('then'), match.group('else')]
        else:
            return None
