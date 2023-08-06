"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

class HistoryUpdateDataModelJSON(object):
    """description of class"""
    def __init__(self, items):
        self._items = items

    def toDict(self):
        jsonItems = []

        for item in self._items:
            jsonItems.append(item.toDict());

        return {'items': jsonItems }


