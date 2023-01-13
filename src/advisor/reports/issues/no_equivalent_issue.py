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

from .issue import Issue
from ..localization import _
from ..report_item import ReportItem


class NoEquivalentIssue(Issue):
    def __init__(self, description, filename=None, lineno=None, item_type=ReportItem.NEUTRAL, function=None):
        super().__init__(description, filename=filename, lineno=lineno, item_type=item_type, function=function)
