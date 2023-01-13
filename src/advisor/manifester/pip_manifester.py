from ..parsers.comment_parser import CommentParser
from ..parsers.continuation_parser import ContinuationParser
from ..parsers.python_comment_parser import PythonCommentParser
from ..parsers.python_requirements_parser import PythonRequirementsParser
from ..helpers.python.python_version_checker import PythonVersionChecker
from .dependency import Dependency

class PipManifester:
    def get_dependencies(self, filename, file_object, report):
        """Get all pip dependencies declared in the requirements.txt file.
        
        Args:
            filename: a str containing the filename of the file to scan.
            file_obj: a stream of text to scan dependencies for.
        
        Returns:
            dependency array: an array of objects of type Dependency."""
        dependencies = []
        continuation_parser = ContinuationParser()
        comment_parser = PythonCommentParser()
        requirements_parser = PythonRequirementsParser()

        for lineno, line in enumerate(file_object, 1):
            line = continuation_parser.parse_line(line)

            if not line:
                continue

            is_comment = comment_parser.parse_line(line)
            if is_comment:
                continue

            dependency_name, used_version, _ = requirements_parser.parse_line(line)
            if dependency_name:
                installed_version = PythonVersionChecker.get_package_version(dependency_name)
                dependency = Dependency(dependency_name, used_version, filename, 'pip', lineno, installed_version)
                dependencies.append(dependency)
        
        return dependencies