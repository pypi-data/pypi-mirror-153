"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

import json
class QueryResultModelJSON(object):
    """description of class"""
    def __init__(self, items, diagnostic, continuationPoint):
      self._items = items
      self._diagnostic = diagnostic
      self._continuationPoint = continuationPoint

    def toDict(self):
        jsonPaths = []

        items = []
        for item in self._items:
            items.append(item.toDict());

        return {'items' : items, 'diagnostic' : self._diagnostic.toDict(), 'continuationPoint': self._continuationPoint }

