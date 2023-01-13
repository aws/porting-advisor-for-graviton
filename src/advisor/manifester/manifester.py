import logging
from ..helpers.rules_loader import RulesLoader
from ..reports.error import Error
from .manifester_factory import ManifesterFactory
from os import listdir, path, walk


class Manifester:
    """This class can get the dependencies declared in a sinfle file, or in all the files from a specified folder."""

    def __init__(self) -> None:
        """Initializes the self._supported_files variable to a dictionary like with all supported files.
        """
        self._supported_files = []
        self._supported_extensions = []
        rules_path = path.abspath(path.join(path.dirname(__file__), '..', 'rules'))
        supported_languages = [filename[:-5] for filename in listdir(rules_path) if path.isfile(path.join(rules_path, filename)) and filename != 'sample.json']
        for language in supported_languages:
            rules = RulesLoader.get_rules(language)
            dependency_files = rules['languageRules'].get('dependencyFiles', [])
            for file in dependency_files:
                if file[:1] == '*':
                    self._supported_extensions.append(file[1:])
                else:
                    self._supported_files.extend(dependency_files)

    def get_dependencies(self, filename, file_object = None, report = None):
        """Gets the dependencies described in the provided filename.

        Args:
            filename: a str containing the filename of the file to scan
            file_obj: a stream of text to scan dependencies for, if available, otherwise, it will open filename
            report: the report being built, if any
        
        Returns:
            dependency array: an array of objects of type Dependency
        """
        # get dependency_scanner
        # return list of dependency:
        #   [(name, version, filename, lineno, installedversion, tool)]
        manifester = ManifesterFactory.get_manifester(filename)
        if file_object == None:
            with open(filename, errors='ignore') as f:
                try:
                    return manifester.get_dependencies(filename, f, report)
                except:
                    logging.error(f'Error while opening: {filename}.', exc_info=True)
        
        return manifester.get_dependencies(filename, file_object, report)

    def scan_folder(self, root_path):
        """Scans a folder and then reviews all supported files for their dependencies.
        
        Args:
            root_path: The folder containing all the source code to review."""
        dependency_files = []
        for dir_name, _, files in walk(root_path):
            for file in files:
                _, extension = path.splitext(file)
                if file in self._supported_files or extension in self._supported_extensions:
                    dependency_files.append(path.join(dir_name, file))
        
        dependencies = []
        for file in dependency_files:
            dependencies.extend(self.get_dependencies(file))
        return dependencies
