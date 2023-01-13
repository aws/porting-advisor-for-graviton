import logging
import subprocess


class PythonVersionChecker():
    def get_package_version(package_name):
        """Get the installed version of a specific package if it's installed

        Args:
            package_name: The name of the package
        
        Returns:
            str: The installed package version
                or None if it's not installed
        """
        try:
            pip_process = subprocess.run(['pip3', 'show', package_name], capture_output=True)
            result = pip_process.stdout.decode('utf-8')
            lines = result.split('\n')
            if (len(lines) > 1):
                version_line = result.split('\n')[1]
                return version_line.split()[1]
        except:
            logging.debug('Error checking python package version.', exc_info=True)
        
        return None

    def get_python_version():
        """Get the installed version of Python via command line

        Returns:
            str: The Python version (e.g. '3.10.4')
                or None if Python is not installed
        """
        try:
            python_process = subprocess.run(['python3', '--version'], capture_output=True)
            if (python_process.stderr != ''):
                python_process = subprocess.run(['python', '--version'], capture_output=True)
            
            result = python_process.stdout.decode('utf-8')
            return result.split()[1]
        except:
            logging.debug('Error checking python version.', exc_info=True)
            return None
    
    def get_pip_version():
        """Get the installed version of pip

        Returns:
            str: The pip version (e.g. '22.1')
                or None if pip is not installed
        """
        try:
            pip_process = subprocess.run(['pip3', '--version'], capture_output=True)
            result = pip_process.stdout.decode('utf-8')
            return result.split()[1]
        except:
            logging.debug('Error checking pip package version.', exc_info=True)
            return None
    