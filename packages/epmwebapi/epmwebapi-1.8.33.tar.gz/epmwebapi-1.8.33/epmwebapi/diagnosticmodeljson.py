"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

class DiagnosticModelJSON(object):
    """description of class"""
    def __init__(self, code):
        self._code = code

    @property
    def code(self):
      return self._code

