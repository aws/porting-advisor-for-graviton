from .regex_manifester import RegexManifester


class NugetManifester(RegexManifester):
    def __init__(self) -> None:
        dependency_re = r'\<PackageReference Include=\"(?P<name>[\w\.\/\-\_]*)\" Version=\"(?P<version>[\w\.\/-]*)\"\s*\/\>'
        super().__init__(dependency_re, 'nuget')