"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

class WriteItemModelJSON(object):
  
  def __init__(self, path, attributeId, value):
    self._path = path
    self._attributeId = attributeId
    self._value = value

  def toDict(self):

    return { 'path': self._path.toDict(), 
             'attributeId': self._attributeId,
             'value': self._value.toDict() }

