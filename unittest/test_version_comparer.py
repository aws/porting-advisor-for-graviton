import unittest
from src.advisor.helpers.version_comparer import VersionComparer


class TestVersionComparer(unittest.TestCase):
    def test_compare_versions_version1_is_newer(self):
        self.assertEqual(1, VersionComparer.compare('1.5.3', '1.4.5'))

    def test_compare_versions_version2_is_newer(self):
        self.assertEqual(-1, VersionComparer.compare('1.5.3', '2.1.0'))

    def test_compare_versions_version1_equals_version2(self):
        self.assertEqual(0, VersionComparer.compare('1.5.3', '1.5.3'))

    def test_compare_versions_with_incomplete_versions(self):
        self.assertEqual(1, VersionComparer.compare('1.5', '1.4.3'))
        self.assertEqual(1, VersionComparer.compare('2.2.1', '1.4'))
        self.assertEqual(1, VersionComparer.compare('2', '1.4.3'))

        self.assertEqual(-1, VersionComparer.compare('1.4.3', '1.5'))
        self.assertEqual(-1, VersionComparer.compare('1.4', '2.2.1'))
        self.assertEqual(-1, VersionComparer.compare('1.4.3', '2'))

        self.assertEqual(1, VersionComparer.compare('2', '1.5'))
        self.assertEqual(-1, VersionComparer.compare('2', '2.2.1'))
    
    def test_compare_versions_with_extra_sections(self):
        self.assertEqual(1, VersionComparer.compare('2.4.9.2', '2.4.9.1'))
        self.assertEqual(1, VersionComparer.compare('2.4.9.2', '2.4.8.2'))
        self.assertEqual(1, VersionComparer.compare('2.4.9.2', '2.3.9.2'))
        self.assertEqual(1, VersionComparer.compare('2.4.9.2', '1.3.9.2'))

        self.assertEqual(-1, VersionComparer.compare('2.4.9.1', '2.4.9.2'))
        self.assertEqual(-1, VersionComparer.compare('2.4.8.2', '2.4.9.2'))
        self.assertEqual(-1, VersionComparer.compare('2.3.9.2', '2.4.9.2'))
        self.assertEqual(-1, VersionComparer.compare('1.3.9.2', '2.4.9.2'))

    def test_compare_versions_with_post_and_dev(self):
        self.assertEqual(1, VersionComparer.compare('2.2.post0', '2.1'))
        self.assertEqual(1, VersionComparer.compare('2.2.post0', '2.2'))
        self.assertEqual(-1, VersionComparer.compare('2.1', '2.2.post0'))
        self.assertEqual(-1, VersionComparer.compare('2.2', '2.2.post0'))

        self.assertEqual(1, VersionComparer.compare('0.22.2.9.dev202207141842065429', '0.22.2.9.dev202207141842065428'))
        self.assertEqual(1, VersionComparer.compare('0.22.2.10', '0.22.2.9.dev202207141842065429'))
        self.assertEqual(-1, VersionComparer.compare('0.22.2.9.dev202207141842065428', '0.22.2.9.dev202207141842065429'))
        self.assertEqual(-1, VersionComparer.compare('0.22.2.9.dev202207141842065429', '0.22.2.10'))

    def test_is_valid_returns_true_for_valid_version(self):
        self.assertTrue(VersionComparer.is_valid('1'))
        self.assertTrue(VersionComparer.is_valid('1.2'))
        self.assertTrue(VersionComparer.is_valid('1.2.3'))
        self.assertTrue(VersionComparer.is_valid('0.22.2.9.dev202207141842065429'))
        self.assertTrue(VersionComparer.is_valid('1.2.3.4'))
    
    def test_is_valid_returns_false_for_invalid_version(self):
        self.assertFalse(VersionComparer.is_valid('4.1.77.Final'))
        self.assertFalse(VersionComparer.is_valid('abc'))