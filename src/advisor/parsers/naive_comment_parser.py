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

class NaiveCommentParser:
    """Naive comment parser."""

    def __init__(self):
        self.in_comment = False
        """Are we in a multi-line comment?"""

    def parse_line(self, line):
        """Parse comments in a source line.

        Args:
            line (str): The line to parse.

        Returns:
            bool: Is this line a comment?
        """
        if line.lstrip().startswith('//'):
            return True
        if self.in_comment:
            if '*/' in line:
                self.in_comment = False
            return True
        else:
            if line.lstrip().startswith('/*'):
                if not '*/' in line:
                    self.in_comment = True
                    return True
                elif line.rstrip().endswith('*/'):
                    return True
        return False
