"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

import json
class QueryResultItemModelJSON(object):
    """description of class"""
    def __init__(self, identity, name, description, typeId):
      self._identity = identity
      self._name = name
      self._typeId = typeId

