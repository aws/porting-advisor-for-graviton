from .issue import Issue


class UnsupportedDependencyIssue(Issue):
    def __init__(self, filename, library_name):
        description = f'dependency library: {library_name} is not supported on Graviton'
        super().__init__(description, filename)