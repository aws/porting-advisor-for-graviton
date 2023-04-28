import logging
import subprocess
from os import path
from ..utils import Utils

class JavaToolInvoker():
    def __init__(self):
        self.JAR_PATH = path.abspath(path.join(path.dirname(__file__), '..', '..', 'tools', 'graviton-ready-java', 'target', 'GravitonReadyAssessor-1.0-SNAPSHOT.jar'))
        self.CLASS_NAME = 'com.amazonaws.labs.GravitonReadyAssessor.Command'

    def can_run(self):
        """Verifies that Java is installed
        
        Returns:
            bool: True if Java is installed, False otherwise
        """
        try:
            java_process = subprocess.run(['java', '--version'], capture_output=True, check=True)
            if (Utils.running_from_binary()):
                return java_process.returncode == 0
            else:
                maven_process = subprocess.run('mvn --version', capture_output=True, check=True, shell=True)
                return java_process.returncode == 0 and maven_process.returncode == 0
                
        except:
            logging.debug('Error checking for java or maven.', exc_info=True)
            return False
    
    def graviton_ready_assessor(self, file_path):
        """Calls the GravitonReadyAssessor tool with the specified path

        Args:
            file_path: The path to the JAR or WAR file
        Returns:
            0, message:  If no native methods are found.
            3, message:  If native methods are found. Message will contain the Native methods found.
            -1, message: If an exception occurrs.
        """
        try:
            if (not self.ensure_jar()):
                return -1, 'Could not generate jar scanner'

            java_process = subprocess.run(['java', '-cp', self.JAR_PATH, self.CLASS_NAME, file_path], capture_output=True)

            if (java_process.returncode == 0):
                return 0, 'No native methods found in scanned JAR files.'

            if java_process.stderr and java_process.returncode != 3:
                raise Exception(java_process.stderr.decode('utf-8'))

            output = java_process.stdout.decode('utf-8')
            lines = output.split('\n')
            
            for line in lines:
                if line.startswith('Native methods:'):
                    return 3, line

            return java_process.returncode
        except:
            logging.debug('Error scanning JAR files.', exc_info=True)
            return -1, f'Error scanning JAR files.'
    
    def ensure_jar(self):
        """Makes sure JAR file exists, otherwise, it creates it
        
        Return:
            bool: True if it exists or it generated successfully
                False otherwise"""
        try:
            if path.isfile(self.JAR_PATH):
                return True
            
            if (Utils.running_from_binary()):
                return False
            
            pom_path = path.abspath(path.join(path.dirname(__file__), '..', '..', 'tools', 'graviton-ready-java', 'pom.xml'))
            logging.debug(f'POM file: {pom_path}')
            mvn_process = subprocess.run(f'mvn package --file {pom_path}', capture_output=True, shell=True)
            if (mvn_process.returncode == 0):
                return True
            
            return False

        except:
            logging.error('Error checking for Graviton Ready JAR file.', exc_info=True)
            return False
