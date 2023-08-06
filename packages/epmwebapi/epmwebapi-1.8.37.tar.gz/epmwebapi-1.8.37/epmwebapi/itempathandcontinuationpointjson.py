"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

class ItemPathAndContinuationPointJSON(object):
    """description of class"""
    def __init__(self, path, continuationPoint, release):
        self._path = path
        self._continuationPoint = continuationPoint
        self._release = release

    def toDict(self):
        return {'path' : self._path.toDict(), 'continuationPoint' : self._continuationPoint, 'release' : self._release}

