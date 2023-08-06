"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

class ReadItemModelJSON(object):
  
  def __init__(self, path, attributeId):
    self._path = path
    self._attributeId = attributeId

  def toDict(self):

    return { 'path': self._path.toDict(), 
             'attributeId': self._attributeId }

