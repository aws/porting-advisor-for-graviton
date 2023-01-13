import logging
import re
import xml.etree.ElementTree as ET
from .dependency import Dependency


class MavenManifester:
    NAME_WITHOUT_NAMESPACE_RE = re.compile(r'(\{.*\})?(?P<name>.*)')
    project_properties = {}

    def get_dependencies(self, filename, file_object, report):
        """Get all pip dependencies declared in the pom.xml file.
        
        Args:
            filename: a str containing the filename of the file to scan
            file_obj: a stream of text to scan dependencies for.
        
        Returns:
            dependency array: an array of objects of type Dependency."""
        try:
            maven_file = ET.parse(file_object)
            project = maven_file.getroot()
            dependencies = []

            # get all property values from the file. they may get used in this or other file's dependency declarations
            for property_node in project.findall('.//{*}properties//*'):
                if property_node.text and property_node.text[0].isdigit():
                    matches = MavenManifester.NAME_WITHOUT_NAMESPACE_RE.search(property_node.tag)
                    property_name = matches.group('name')
                    value = property_node.text
                    MavenManifester.project_properties[property_name] = value

            for dependency in project.findall('.//{*}dependencies//{*}dependency'):
                artifact_id = dependency.find('.//{*}artifactId').text
                versionElement = dependency.find('.//{*}version')
                version = None
                if not versionElement == None:
                    version = versionElement.text

                    # version is a variable pointing to the properties section
                    if version.startswith(r'${'):
                        # get the name from '${name}'
                        property_name = version[2:len(version)-1]
                        if property_name in self.project_properties:
                            version = self.project_properties[property_name]
                
                item = Dependency(artifact_id, version, filename, 'maven')
                dependencies.append(item)
            return dependencies
        except:
            logging.error(f'Failed to parse file: {filename}.', exc_info=True)