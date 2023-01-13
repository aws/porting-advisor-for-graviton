import os
import unittest
import urllib.request
from src.advisor.helpers.java.java_tool_invoker import JavaToolInvoker


class TestJavaToolIncoker(unittest.TestCase):
    def setUp(self) -> None:
        self.tool_invoker = JavaToolInvoker()

    def test_can_run_checks_java_is_installed(self):
        self.assertTrue(self.tool_invoker.can_run())
    
    def test_graviton_ready_assessor_for_jars_with_native_methods(self):
        download_url = 'https://repo1.maven.org/maven2/io/netty/netty-transport-native-unix-common/4.1.73.Final/netty-transport-native-unix-common-4.1.73.Final.jar'
        path = os.path.join('sample-projects', 'java-samples', 'netty-transport-native-unix-common-4.1.73.Final.jar')
        urllib.request.urlretrieve(download_url, path)
        result, message = self.tool_invoker.graviton_ready_assessor(path)
        os.remove(path)
        self.assertEqual(3, result)
        self.assertTrue(message.startswith('Native methods:'))

    def test_graviton_ready_assessor_for_jars_with_non_native_methods(self):
        download_url = 'https://search.maven.org/remotecontent?filepath=javax/activation/activation/1.1.1/activation-1.1.1.jar'
        path = os.path.join('sample-projects', 'java-samples', 'activation-1.1.1.jar')
        urllib.request.urlretrieve(download_url, path)
        result, message = self.tool_invoker.graviton_ready_assessor(path)
        os.remove(path)
        self.assertEqual(0, result)
        self.assertEqual('No native methods found in scanned JAR files.', message)