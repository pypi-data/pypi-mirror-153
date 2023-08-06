"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

import requests
import json

class Resource(object):

  def __init__(self, resourcesManager, id, name, description, mimeType):
    self._resourcesManager = resourcesManager
    self._id = id
    self._name = name
    self._description = description
    self._mimeType = mimeType

  def download(self, type):

    return self._resourcesManager._download(self._id, type)

  def upload(self, file):

    return self._resourcesManager._updateFile(self._id, self._name, self._mimeType, file)

  def delete(self):

    return self._resourcesManager._delete(self._id)


