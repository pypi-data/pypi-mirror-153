"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

import json
class QueryModelJSON(object):
    """description of class"""
    def __init__(self, continuationPoint, release, resultMask, browseNameFilter, descriptionFilter, euNameFilter, typeFilter, domainFilter):
      self._continuationPoint = continuationPoint
      self._release = release
      self._resultMask = resultMask
      self._browseNameFilter = browseNameFilter
      self._descriptionFilter = descriptionFilter
      self._euNameFilter = euNameFilter
      self._typeFilter = typeFilter
      self._domainFilter = domainFilter

    def toDict(self):
        jsonPaths = []

        types = []
        for item in self._typeFilter:
            types.append(item.toDict());

        return {'continuationPoint': self._continuationPoint, 'release': self._release, 
               'resultMask' : self._resultMask, 'browseNameFilter' : self._browseNameFilter, 
               'descriptionFilter' : self._descriptionFilter, 'euNameFilter' : self._euNameFilter, 
               'typeFilter' : types, 'domainFilter' : self._domainFilter }

