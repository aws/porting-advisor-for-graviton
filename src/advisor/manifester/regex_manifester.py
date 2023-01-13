import re
from .dependency import Dependency


class RegexManifester:
    def __init__(self, pattern, tool):
        self.dependencies_re = pattern
        self.tool = tool
    
    def get_dependencies(self, filename, file_object, report):
        """Get all dependencies matching the provided regular expression.
        
        Args:
            filename: a str containing the filename of the file to scan.
            file_obj: a stream of text to scan dependencies for, if available, otherwise, it will open filename.
        
        Returns:
            dependency array: an array of objects of type Dependency."""
        file_object.seek(0)
        file_contents = file_object.read()
        matches = re.finditer(self.dependencies_re, file_contents, re.MULTILINE)
        dependencies = []

        for _, match in enumerate(matches):
            dependency = Dependency(match.group('name'), match.group('version'), filename, self.tool)
            dependencies.append(dependency)
        
        return dependencies
