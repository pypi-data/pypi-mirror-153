"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

class BrowseModelJSON(object):

  def __init__(self, items, continuationPoint):
    self._items = items
    self._continuationPoint = continuationPoint

  def toDict(self):
    jsonPaths = []

    childMap = []
    for item in self._items:
        childMap.append(item.toDict());

    return {'items': childMap, 'continuationPoint': self._continuationPoint }
