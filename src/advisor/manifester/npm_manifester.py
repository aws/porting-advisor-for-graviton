import json
from .dependency import Dependency


class NpmManifester:
    def get_dependencies(self, filename, file_object, report):
        """Get all npm dependencies declared in the package.json file.
        
        Args:
            filename: a str containing the filename of the file to scan.
            file_obj: a stream of text to scan dependencies for, if available, otherwise, it will open filename.
        
        Returns:
            dependency array: an array of objects of type Dependency."""
        dependencies = []
        package_json = json.load(file_object)

        packages = package_json.get('dependencies', {})
        packages.update(package_json.get('devDependencies', {}))
        for key in packages:
            dependency = Dependency(key, packages[key], filename, 'npm')
            dependencies.append(dependency)
        
        return dependencies