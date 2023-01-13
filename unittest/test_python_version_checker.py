import pkg_resources
import platform
import unittest
from src.advisor.helpers.python.python_version_checker import PythonVersionChecker

class TestPythonVersionChecker(unittest.TestCase):
    def test_get_package_version_returns_non_empty_string_for_existing_library(self):
        pip_version = pkg_resources.get_distribution('Jinja2').version
        self.assertEqual(pip_version, PythonVersionChecker.get_package_version('Jinja2'))

    def test_get_package_version_returns_none_for_fake_library(self):
        version = PythonVersionChecker.get_package_version('myFakeLibraryThatDoesNotExist')
        self.assertIsNone(version)
    
    def test_get_python_version_returns_current_version(self):
        runtime_version = platform.python_version()
        self.assertEqual(runtime_version, PythonVersionChecker.get_python_version())
    
    def test_get_pip_version_returns_current_version(self):
        pip_version = pkg_resources.get_distribution('pip').version
        self.assertEqual(pip_version, PythonVersionChecker.get_pip_version())