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

class ContinuationParser:
    """Continuation parser. Parses lines ending with \ as continuations."""

    def __init__(self):
        self.continuation_line = None

    def parse_line(self, line):
        """Parse continuations in a source line.

        Args:
            line (str): The line to parse.

        Returns:
            str: THe concatenated line, or None if a continuation is in progress.
        """
        # Lines ending with \ are not processed immediately, but are concatenated together until a line not ending in
        # \ is encountered. This means that issues reported against the line will have the line number of the final continuation liner rather than the first.
        if line.endswith('\\') or line.endswith('\\\n'):
            if self.continuation_line:
                self.continuation_line += line.rstrip()[:-1]
            else:
                self.continuation_line = line.rstrip()[:-1]
            return None
        elif self.continuation_line:
            line = self.continuation_line + line
            self.continuation_line = None
        return line
