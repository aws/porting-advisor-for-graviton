import unittest
from src.advisor.helpers.rules_loader import RulesLoader

class TestRulesLoader(unittest.TestCase):
    def test_get_rules_gets_valid_object_for_existing_rules_file(self):
        rules = RulesLoader.get_rules('python')
        name = rules['languageRules']['name']
        self.assertIsNotNone(rules)
        self.assertEqual('Python', name)

    def test_get_rules_gets_none_for_unexisting_file(self):
        rules = RulesLoader.get_rules('fake_language')
        self.assertIsNone(rules)