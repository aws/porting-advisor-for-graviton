import json
from os import path

class RulesLoader():
    
    def get_rules(language_name):
        """Gets the rules object for the specified language.
    
        Args:
            language_name: a str with the name of the language.
        Returns:
            object: a representation of the JSON rule file for the language. None if the rules file is not found."""
        rules_file = path.abspath(path.join(path.dirname(__file__), '..', 'rules', f'{language_name}.json'))
        if path.isfile(rules_file):
            with open(rules_file, 'r') as rules_file_content:
                rules = json.load(rules_file_content)
                return rules
        else:
            return None