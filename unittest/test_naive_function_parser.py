"""
Copyright 2018 Arm Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

SPDX-License-Identifier: Apache-2.0
"""

import unittest
from src.advisor.parsers.naive_function_parser import NaiveFunctionParser


class TestNaiveFunctiontParser(unittest.TestCase):
    def test_parse_line(self):
        function_parser = NaiveFunctionParser()
        function_parser.parse_line('not a function definition')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('int function_declaration(int arg1);')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('not a function definition')
        self.assertIsNone(function_parser.current_function)

        function_parser.parse_line('int single_line_function_definition(int arg1) {')
        self.assertEqual(function_parser.current_function, 'single_line_function_definition')
        function_parser.parse_line('    function body')
        self.assertEqual(function_parser.current_function, 'single_line_function_definition')
        function_parser.parse_line('}')
        self.assertIsNone(function_parser.current_function)

        function_parser.parse_line('int')
        function_parser.parse_line('multi_line_function_definition1(int arg1) {')
        self.assertEqual(function_parser.current_function, 'multi_line_function_definition1')
        function_parser.parse_line('    function body')
        self.assertEqual(function_parser.current_function, 'multi_line_function_definition1')
        function_parser.parse_line('}')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('int')
        function_parser.parse_line('multi_line_function_definition2')
        function_parser.parse_line('(int arg1) {')
        self.assertEqual(function_parser.current_function, 'multi_line_function_definition2')
        function_parser.parse_line('    function body')
        self.assertEqual(function_parser.current_function, 'multi_line_function_definition2')
        function_parser.parse_line('}')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('int')
        function_parser.parse_line('multi_line_function_definition3')
        function_parser.parse_line('(int arg1)')
        function_parser.parse_line('{')
        self.assertEqual(function_parser.current_function, 'multi_line_function_definition3')
        function_parser.parse_line('    function body')
        self.assertEqual(function_parser.current_function, 'multi_line_function_definition3')
        function_parser.parse_line('}')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('int')
        function_parser.parse_line('multi_line_function_definition4')
        function_parser.parse_line('(')
        function_parser.parse_line('int arg1')
        function_parser.parse_line(')')
        function_parser.parse_line('{')
        self.assertEqual(function_parser.current_function, 'multi_line_function_definition4')
        function_parser.parse_line('    function body')
        self.assertEqual(function_parser.current_function, 'multi_line_function_definition4')
        function_parser.parse_line('}')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('int')
        function_parser.parse_line('multi_line_function_definition5')
        function_parser.parse_line('(')
        function_parser.parse_line('int arg1, ')
        function_parser.parse_line('int arg2')
        function_parser.parse_line(')')
        function_parser.parse_line('{')
        self.assertEqual(function_parser.current_function, 'multi_line_function_definition5')
        function_parser.parse_line('    function body')
        self.assertEqual(function_parser.current_function, 'multi_line_function_definition5')
        function_parser.parse_line('}')
        self.assertIsNone(function_parser.current_function)

        # nesting
        function_parser.parse_line('int func() {')
        self.assertEqual(function_parser.current_function, 'func')
        function_parser.parse_line('    for (int i=0;i<10;i++) {')
        self.assertEqual(function_parser.current_function, 'func')
        function_parser.parse_line('        printf("%d\n", i);')
        self.assertEqual(function_parser.current_function, 'func')
        function_parser.parse_line('    }')
        self.assertEqual(function_parser.current_function, 'func')
        function_parser.parse_line('}')
        self.assertIsNone(function_parser.current_function)

        function_parser.parse_line('int func() {')
        self.assertEqual(function_parser.current_function, 'func')
        function_parser.parse_line('    if (blah) {')
        self.assertEqual(function_parser.current_function, 'func')
        function_parser.parse_line('        foo')
        self.assertEqual(function_parser.current_function, 'func')
        function_parser.parse_line('    } else if (blah) {')
        function_parser.parse_line('        bar')
        self.assertEqual(function_parser.current_function, 'func')
        function_parser.parse_line('    }')
        self.assertEqual(function_parser.current_function, 'func')
        function_parser.parse_line('}')
        self.assertIsNone(function_parser.current_function)

    @unittest.expectedFailure
    def test_function_definiton_like_macro(self):
        # the parser doesn't handle macros that look like function declarations but are actually for / while loops.
        function_parser.parse_line('MACRO(x,y,z) {')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('    body')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('}')
        self.assertIsNone(function_parser.current_function)

    def test_single_line_function(self):
        function_parser = NaiveFunctionParser()
        function_parser.parse_line('not a function definition')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('int single_line_function() { }')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('not a function definition')
        self.assertIsNone(function_parser.current_function)

    def test_class_method(self):
        function_parser = NaiveFunctionParser()
        function_parser.parse_line('not a function definition')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('int myclass::method() {')
        self.assertEqual(function_parser.current_function, 'myclass::method')
        function_parser.parse_line('    foo')
        self.assertEqual(function_parser.current_function, 'myclass::method')
        function_parser.parse_line('}')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('not a function definition')
        self.assertIsNone(function_parser.current_function)

    def test_class_method_2(self):
        function_parser = NaiveFunctionParser()
        function_parser.parse_line('not a function definition')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('void MyClass::myMethod(const String &arg)')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('{')
        self.assertEqual(function_parser.current_function, 'MyClass::myMethod')
        function_parser.parse_line('    foo')
        self.assertEqual(function_parser.current_function, 'MyClass::myMethod')
        function_parser.parse_line('}')
        self.assertIsNone(function_parser.current_function)
        function_parser.parse_line('not a function definition')
        self.assertIsNone(function_parser.current_function)
