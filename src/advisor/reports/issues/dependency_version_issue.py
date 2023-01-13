from .issue import Issue


class DependencyVersionIssue(Issue):
    def __init__(self, filename, lineno, library_name, current_version, suggested_version):
        description = f'using dependency library {library_name} version {current_version}. upgrade to at least version {suggested_version}'
        super().__init__(description=description, filename=filename,
                         lineno=lineno)