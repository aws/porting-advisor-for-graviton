import re
from ..parsers.ruby_gem_parser import RubyGemParser
from .dependency import Dependency


class RubyManifester():
    GEM_RE =r'gem (?P<declaration>.*)'

    def get_dependencies(self, filename, file_object, report):
        """Get all ruby dependencies declared in the Gemfile file.
        
        Args:
            filename: a str containing the filename of the file to scan.
            file_obj: a stream of text to scan dependencies for, if available, otherwise, it will open filename.
        
        Returns:
            dependency array: an array of objects of type Dependency."""
        dependencies = []
        gem_parser = RubyGemParser()
        matches = re.finditer(RubyManifester.GEM_RE, file_object.read(), re.MULTILINE)
        
        for _, match in enumerate(matches):
            name, version = gem_parser.parse_line(match.group('declaration'))
            if name:
                dependency = Dependency(name, version, filename, 'ruby')
                dependencies.append(dependency)
        
        return dependencies
