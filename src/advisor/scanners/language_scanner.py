from os import path
from ..helpers.rules_loader import RulesLoader
from ..helpers.version_comparer import VersionComparer
from ..manifester.dependency import Dependency
from ..reports.issues.dependency_version_issue import DependencyVersionIssue
from ..reports.issues.unsupported_dependency_issue import UnsupportedDependencyIssue
from ..reports.remarks.dependency_version_remark import DependencyVersionRemark
from ..reports.remarks.language_version_remark import LanguageVersionRemark
from ..reports.remarks.special_instructions_remark import SpecialInstructionsRemark
from ..reports.remarks.tool_version_remark import ToolVersionRemark
from .scanner import Scanner


class LanguageScanner(Scanner):
    """Base class for language scanners that focus on checking versions of dependency libraries."""
    
    def __init__(self) -> None:
        self.DESCRIPTION = ''
        self.LANGUAGE_RULES = {}
        self.TOOLS_RULES = dict()
        self.LIBRARY_RULES = dict()
        self.SOURCE_EXTENSION = []
        self.MIN_VERSION = ''
        self.RECOMMENDED_VERSION = ''
        self.INSTALLED_VERSION = ''
        self.DETAILS_URL = ''
        self.DEPENDENCY_FILES = []
        self.OVERRIDE_TEXT = ''
        self._added_language_version_remark = False
        self.load_rules()

    def load_rules(self):
        """Loads the rules file if the RULES_FILE property is set in the subclass."""
        rules = RulesLoader.get_rules(self.LANGUAGE_NAME)         
        self.assign_values(rules)
  
    def assign_values(self, rules):
        """Assigns the values read from the rules file."""
        if rules:
            self.LANGUAGE_RULES = rules['languageRules']
            self.DESCRIPTION = self.LANGUAGE_RULES.get('description', '')
            self.SOURCE_EXTENSION = self.LANGUAGE_RULES.get('extensions', [])
            self.MIN_VERSION = self.LANGUAGE_RULES.get('minVersion', '')
            self.RECOMMENDED_VERSION = self.LANGUAGE_RULES.get('recommendedVersion', '')
            self.DETAILS_URL = self.LANGUAGE_RULES.get('detailsUrl', '')
            self.DEPENDENCY_FILES = self.LANGUAGE_RULES.get('dependencyFiles', [])
            self.OVERRIDE_TEXT = self.LANGUAGE_RULES.get('overrideText', '')
            
            tool_rules = rules.get('toolsRules', None)
            if tool_rules:
                for tool in tool_rules:
                    self.TOOLS_RULES[tool['name']] = tool
            
            library_rules = rules.get('libraryRules', None)
            if library_rules:
                for library in library_rules:
                    self.LIBRARY_RULES[library['name'].casefold()] = library
    
    def accepts_file(self, filename):
        """ Determines if this scanner will be used for a given file.

        Args:
            filename: The name of the file to check.

        Returns:
            bool: True if this scanner can assess the provided file, False otherwise.
        """
        filename_and_extension = path.basename(filename)
        is_valid_file = filename_and_extension.lower() in self.DEPENDENCY_FILES
        return is_valid_file or self.has_source_extension(filename)
    
    def has_source_extension(self, filename):
        """Determines if a file has this language extension."""
        _, ext = path.splitext(filename)
        return ext in self.SOURCE_EXTENSION
    
    def add_language_remarks(self, report):
        """Adds the language version recommendations.

        Args:
            report: The report to add the remark to.
        """
        if not self._added_language_version_remark:
            report.add_remark(LanguageVersionRemark(language_name=self.LANGUAGE_NAME,
                                                    min_version=self.MIN_VERSION,
                                                    details=self.DESCRIPTION,
                                                    recommended_version=self.RECOMMENDED_VERSION,
                                                    installed_version=self.INSTALLED_VERSION,
                                                    details_url=self.DETAILS_URL,
                                                    override_text=self.OVERRIDE_TEXT))
            self.add_tool_remarks(report)
            self._added_language_version_remark = True
    
    def add_tool_remarks(self, report):
        """Add configured tool remarks for this language to the report."""
        for tool in self.TOOLS_RULES:
            report.add_remark(
                ToolVersionRemark(self.TOOLS_RULES[tool].get('details'),
                                self.TOOLS_RULES[tool].get('minVersion'),
                                self.TOOLS_RULES[tool].get('recommendedVersion'),
                                self.TOOLS_RULES[tool].get('installedVersion'),
                                self.TOOLS_RULES[tool].get('detailsUrl'),
                                self.TOOLS_RULES[tool].get('overrideText')))
    
    def add_library_remarks(self, libraries: list[Dependency], report):
        """Adds the dependency libraries remarks.
        
        Args:
            dependencies: The list of dependencies to add.
            report: The report to add the remarks to.
        """
        for library in libraries:
            library_name = library.name.casefold()
            used_version = library.version
            filename = library.filename
            lineno = library.lineno
            installed_version = library.installed_version

            if library_name in self.LIBRARY_RULES:
                unsupported = self.LIBRARY_RULES[library_name].get('unsupported', False)
                if unsupported:
                    report.add_issue(UnsupportedDependencyIssue(filename, library_name))
                    continue
                
                special_instructions = self.LIBRARY_RULES[library_name].get('specialInstructions')
                if special_instructions:
                    details_url = self.LIBRARY_RULES[library_name].get('detailsUrl')
                    report.add_remark(SpecialInstructionsRemark(filename, library_name, special_instructions, details_url))
                    continue

                min_version = self.LIBRARY_RULES[library_name].get('minVersion', '')
                if used_version and VersionComparer.is_valid(used_version):
                    if VersionComparer.compare(used_version, min_version) == -1:
                        report.add_issue(
                            DependencyVersionIssue(filename, lineno, library_name, used_version, min_version))
                else:
                    if installed_version and VersionComparer.compare(installed_version, min_version) == -1:
                        report.add_issue(DependencyVersionIssue(filename, lineno, library_name, installed_version,
                                                                min_version))
                    else:
                        report.add_remark(DependencyVersionRemark(filename,
                                                                lineno,
                                                                library_name,
                                                                min_version=min_version,
                                                                installed_version=installed_version))

            continue