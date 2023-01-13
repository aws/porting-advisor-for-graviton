"""
Copyright 2017-2018 Arm Ltd.

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

import re
from ...constants.arch_strings import *


class PreprocessorDirective:
    """Information about a preprocessor directive."""
    TYPE_CONDITIONAL = '#if'
    TYPE_ERROR       = '#error'
    TYPE_PRAGMA      = '#pragma'
    TYPE_DEFINE      = '#define'
    TYPE_OTHER       = 'other'
    TYPE_INVALID     = 'invalid'

    def __init__(self, directive_type, if_line=None, is_compiler=None, macro_name=None, body=None):
        self.directive_type = directive_type
        """
        The type of directive:
        
        TYPE_CONDITIONAL - a #if directive.
        TYPE_ERROR       - a #error directive.
        TYPE_PRAGMA      - a #pragma directive.
        TYPE_DEFINE      - a #define directive. 
        TYPE_OTHER       - some other directive.
        TYPE_INVALID     - an invalid directive.
        """
        self.if_line = if_line
        """The line that opened the current preprocessor block."""
        self.is_compiler = is_compiler
        """True if the current preprocessor block is compiler-speciifc, else False."""
        self.macro_name = macro_name
        """Macro name used in #ifdef, #define."""
        self.body = body
        """#define macro body."""


class NaiveCpp:
    """Naive C preprocessor. This class is used by SourceScanner to determine
    which source lines will/will not be compiled on aarch64 platorms."""

    TOKEN_PROG = re.compile(
        r'((?:!\s*)?defined\s*\(\s*\w+\s*\)|(?:!\s*)?\w+|\|\||\&\&|\(|\)|\s+)')
    """Regular expression to tokenize C preprocessor directives."""
    DEFINED_PROG = re.compile(r'(?:(!)\s*)?defined\s*\(\s*(\w+)\s*\)')
    """Regular expression to match (possibly negated) defined(macro)
    expressions."""
    MACRO_PROG = re.compile(r'(?:(!)\s*)?(\w+)')
    """Regular expression to match (possibly negated) macro expressions."""
    AARCH64_MACROS_RE_PROG = re.compile(r'(?:\w*_|^)(%s)(?:_\w*|$)' %
                                        '|'.join(AARCH64_ARCHS),
                                        re.IGNORECASE)
    """Regular expression to match aarch64 predefined macros."""
    NON_AARCH64_MACROS_RE_PROG = re.compile(r'(?:\w*_|^)(%s)(?:_\w*|$)' %
                                            '|'.join(NON_AARCH64_ARCHS),
                                            re.IGNORECASE)
    """Regular expression to match non-aarch64 architecture predefined
    macros."""
    COMPILER_MACROS_RE_PROG = re.compile(r'(?:\w*_|^)(%s)(?:_\w*|$)' %
                                         '|'.join(COMPILERS),
                                         re.IGNORECASE)
    """Regular expression to match compiler macros."""
    IGNORE_MACROS = ['_M_HYBRID_X86_ARM64']
    """Special-cased macros to ignore because they confuse the parser."""

    def __init__(self):
        self.in_aarch64 = []
        """
        Stack of preprocessor block states. When a new preprocessor block is begun with #if or #ifdef a new state
        is pushed onto the stack. The state is True if the condition contains a macro defined on aarch64, False
        if the condition contains the negation of a macro defined on aarch64, and None (undefined) otherwise. When the
        preprocessor block is finished with #endif the state is popped.
        """
        self.in_other_arch = []
        """
        Stack of preprocessor block states. When a new preprocessor block is begun with #if or #ifdef a new state
        is pushed onto the stack. The state is True if the condition contains a macro defined on a non-aarch64
        architecture, False if the condition contains the negation of a macro defined on a non-aarch64 architecture, and
        None (undefined) otherwise. When the preprocessor block is finished with #endif the state is popped.
        """
        self.in_compiler = []
        """
        Stack of preprocessor block states. When a new preprocessor block is begun with #if or #ifdef a new state
        is pushed onto the stack. The state is True if the condition contains a compiler-specific macro, else False.
        When the preprocessor block is finished with #endif the state is popped.
        """
        self.if_lines = []
        """
        A stack of preprocessor block control statements. When a new preprocessor block is begun with #if or #ifdef
        the statement is pushed onto the stack. When the preprocessor block is finished with #endif the statement
        is popped.
        """
        self.seen_aarch64 = []
        """
        Stack of preprocessor block states. Have we seen an aarch64-specific block at this level?
        """
        self.seen_other_arch = []
        """
        Stack of preprocessor block states. Have we seen a non-aarch64-specific block at this level
        """

    def parse_line(self, line):
        """Parse preprocessor directives in a source line.

        Args:
            line (str): The line to parse.

        Returns:
            PreprocessorDirective: Information about the parsed directive. 
        """
        if line.lstrip().startswith('#'):
            return self._parse_directive_line(line)
        else:
            return PreprocessorDirective(directive_type=None)

    def _parse_directive_line(self, line):
        parts = line.lstrip().split(maxsplit=1)
        directive = parts[0][1:]
        if directive == 'error':
            return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_ERROR)
        elif directive == 'pragma':
            return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_PRAGMA)
        elif directive == 'define':
            if len(parts) == 1:
                return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_INVALID)
            rest = parts[1]
            if rest:
                define_parts = rest.lstrip().split(maxsplit=1)
            else:
                define_parts = []
            macro_name = define_parts[0]
            body = define_parts[1] if len(define_parts) > 1 else None
            return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_DEFINE,
                                        macro_name=macro_name, body=body)
        elif directive == 'if':
            if len(parts) == 1:
                return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_INVALID)
            expression = parts[1]
            self.in_aarch64.append(NaiveCpp._is_expression_aarch64(expression))
            self.seen_aarch64.append(self.in_aarch64[-1])
            self.in_other_arch.append(
                NaiveCpp._is_expression_non_aarch64(expression))
            self.seen_other_arch.append(self.in_other_arch[-1])
            is_compiler = NaiveCpp._is_expression_compiler(expression)
            self.in_compiler.append(is_compiler)
            self.if_lines.append(line)
            return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_CONDITIONAL, if_line=line,
                                         is_compiler=is_compiler)
        elif directive == 'elif':
            if len(parts) == 1:
                return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_INVALID)
            expression = parts[1]
            if self.in_aarch64:
                self.in_aarch64[-1] = \
                    NaiveCpp._is_expression_aarch64(expression)
            if self.seen_aarch64:
                self.seen_aarch64[-1] = self.in_aarch64[-1] if self.seen_aarch64[-1] is None else \
                    self.seen_aarch64[-1] or self.in_aarch64[-1]
            if self.in_other_arch:
                self.in_other_arch[-1] = \
                    NaiveCpp._is_expression_non_aarch64(expression)
            if self.seen_other_arch:
                self.seen_other_arch[-1] = self.in_other_arch[-1] if self.seen_other_arch[-1] is None else \
                    self.seen_other_arch[-1] or self.in_other_arch[-1]
            if self.in_compiler:
                is_compiler = NaiveCpp._is_expression_compiler(expression)
                self.in_compiler[-1] = \
                    is_compiler
            else:
                is_compiler = False
            return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_CONDITIONAL, if_line=line,
                                         is_compiler=is_compiler)
        elif directive == 'ifdef':
            if len(parts) == 1:
                return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_INVALID)
            macro = parts[1]
            self.in_aarch64.append(
                NaiveCpp.AARCH64_MACROS_RE_PROG.match(macro) is not None or None)
            self.seen_aarch64.append(self.in_aarch64[-1])
            self.in_other_arch.append(
                NaiveCpp.NON_AARCH64_MACROS_RE_PROG.match(macro) is not None or None)
            self.seen_other_arch.append(self.in_other_arch[-1])
            is_compiler = NaiveCpp.COMPILER_MACROS_RE_PROG.match(
                macro) is not None or None
            self.in_compiler.append(is_compiler)
            self.if_lines.append(line)
            return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_CONDITIONAL, if_line=line,
                                         is_compiler=is_compiler, macro_name=macro)
        elif directive == 'ifndef':
            if len(parts) == 1:
                return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_INVALID)
            macro = parts[1]
            self.in_aarch64.append(
                False if NaiveCpp.AARCH64_MACROS_RE_PROG.match(macro) is not None else None)
            self.seen_aarch64.append(self.in_aarch64[-1])
            self.in_other_arch.append(
                False if NaiveCpp.NON_AARCH64_MACROS_RE_PROG.match(macro) is not None else None)
            self.seen_other_arch.append(self.in_other_arch[-1])
            is_compiler = False if NaiveCpp.COMPILER_MACROS_RE_PROG.match(
                macro) else None
            self.in_compiler.append(is_compiler)
            self.if_lines.append(line)
            return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_CONDITIONAL, if_line=line,
                                         is_compiler=is_compiler, macro_name=macro)
        elif directive == 'else':
            if self.in_aarch64:
                self.in_aarch64[-1] = \
                    not self.seen_aarch64[-1] if self.seen_aarch64[-1] is not None else None
            if self.in_other_arch:
                self.in_other_arch[-1] = \
                    None if self.seen_aarch64[-1] else \
                        (not self.seen_other_arch[-1] if self.seen_other_arch[-1] is not None else None)
            if self.in_compiler:
                self.in_compiler[-1] = \
                    NaiveCpp.tri_negate(
                        self.in_compiler[-1])
            if self.if_lines:
                if_line = self.if_lines[-1]
            else:
                if_line = line
            return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_CONDITIONAL, if_line=if_line)
        elif directive == 'endif':
            if self.in_aarch64:
                self.in_aarch64.pop()
            if self.seen_aarch64:
                self.seen_aarch64.pop()
            if self.in_other_arch:
                self.in_other_arch.pop()
            if self.seen_other_arch:
                self.seen_other_arch.pop()
            if self.in_compiler:
                self.in_compiler.pop()
            if self.if_lines:
                if_line = self.if_lines.pop()
            else:
                if_line = None
            return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_CONDITIONAL, if_line=if_line)
        else:
            return PreprocessorDirective(directive_type=PreprocessorDirective.TYPE_OTHER)

    @staticmethod
    def tri_negate(x):
        if x is None:
            return None
        else:
            return not x

    @staticmethod
    def _is_expression_x(expression, x):
        tokens = NaiveCpp.TOKEN_PROG.split(expression)
        for token in tokens:
            match = NaiveCpp.DEFINED_PROG.match(token)
            if not match:
                match = NaiveCpp.MACRO_PROG.match(token)
            if match:
                negated = match.group(1) == '!'
                macro = match.group(2)
                if macro in NaiveCpp.IGNORE_MACROS:
                    continue
                if x.match(macro) is not None:
                    return not negated
        return None

    @staticmethod
    def _is_expression_aarch64(expression):
        return NaiveCpp._is_expression_x(expression, NaiveCpp.AARCH64_MACROS_RE_PROG)

    @staticmethod
    def _is_expression_non_aarch64(expression):
        return NaiveCpp._is_expression_x(expression, NaiveCpp.NON_AARCH64_MACROS_RE_PROG)

    @staticmethod
    def _is_expression_compiler(expression):
        return NaiveCpp._is_expression_x(expression, NaiveCpp.COMPILER_MACROS_RE_PROG)

    @staticmethod
    def _in_x_code(x):
        return True in x

    @staticmethod
    def _in_x_else_code(x):
        return False in x

    def in_aarch64_specific_code(self):
        """
        Are we in aarch64 specific code?

        Returns:
            bool: True if we are currently in an #ifdef __aarch64_ or similar block, else False. 
        """
        return NaiveCpp._in_x_code(self.in_aarch64)

    def in_other_arch_specific_code(self):
        """
        Are we in other architecture (non-aarch64) specific code?

        Returns:
            bool: True if we are currently in an #ifdef OTHERARCH or similar block, else False. 
        """
        return NaiveCpp._in_x_code(self.in_other_arch)

    def in_other_arch_else_code(self):
        """
        Are we in the #else block of other architecture (non-aarch64) specific code?

        Returns:
            bool: True if we are currently in the #else block of an #ifdef OTHERARCH or similar block, else False.
        """
        return NaiveCpp._in_x_else_code(self.in_other_arch)

    def in_compiler_specific_code(self):
        """
        Are we in compiler specific code?

        Returns:
            bool: True if we are currently in an #ifdef COMPILER or similar block, else False. 
        """
        return NaiveCpp._in_x_code(self.in_compiler)
