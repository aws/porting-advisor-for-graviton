from .regex_manifester import RegexManifester


class GoManifester(RegexManifester):
    def __init__(self) -> None:
        dependency_re = r'\t(?P<name>[\w\.\/\-\_]*) v(?P<version>[\w\.\/-]*)'
        super().__init__(dependency_re, 'go')