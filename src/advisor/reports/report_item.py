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

from .localization import _


class ReportItem:
    SUMMARY = 'summary'
    POSITIVE = 'positive'
    NEUTRAL = 'neutral'
    NEGATIVE = 'negative'
    ERROR = 'error'
    TYPES = [SUMMARY, POSITIVE,
             NEGATIVE, NEUTRAL,
             ERROR]

    def __init__(self, description, filename=None, lineno=None, item_type=NEUTRAL, function=None):
        self.filename = filename
        self.lineno = lineno
        self.description = description
        self.item_type = item_type
        self.function = function

    def __str__(self):
        if self.lineno:
            if self.function:
                return _('%(file)s:%(lineno)s (%(function)s): %(description)s') % \
                    {'file': self.filename,
                     'lineno': self.lineno,
                     'function': self.function,
                     'description': self.description}
            else:
                return _('%(file)s:%(lineno)s: %(description)s') % \
                    {'file': self.filename,
                     'lineno': self.lineno,
                     'description': self.description}
        elif self.filename:
            if self.function:
                return _('%(file)s (%(function)s): %(description)s') % \
                    {'file': self.filename,
                     'function': self.function,
                     'description': self.description}
            else:
                return _('%(file)s: %(description)s') % \
                    {'file': self.filename,
                     'description': self.description}
        else:
            if self.function:
                return _('%(function)s: %(description)s') % \
                    {'function': self.function,
                     'description': self.description}
            else:
                return _('%(description)s') % \
                    {'description': self.description}
