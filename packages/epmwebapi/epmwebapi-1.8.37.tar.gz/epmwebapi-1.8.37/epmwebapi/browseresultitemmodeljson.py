"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

class BrowseResultItemModelJSON(object):

  def __init__(self, identity, displayName, relativePath, type, nodeClass):
    self._identity = identity
    self._displayName = displayName
    self._relativePath = relativePath
    self._type = type
    self._nodeClass = nodeClass

