class Dependency:
    def __init__(self, name, version, filename, tool, lineno = None, installed_version = None) -> None:
        self.name = name
        self.version = version
        self.filename = filename
        self.tool = tool
        self.lineno = lineno
        self.installed_version = installed_version