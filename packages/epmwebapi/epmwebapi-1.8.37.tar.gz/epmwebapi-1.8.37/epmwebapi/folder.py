"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

import requests
import json

class Folder(object):

  def __init__(self, resourcesManager, id, name, description):
    self._resourcesManager = resourcesManager
    self._id = id
    self._name = name
    self._description = description


  def browse(self):

    return self._resourcesManager._browse(self._id)

  def upload(self, name, file, description = None, mimeType = None, thumbnail = None, thumbnailMimeType = None, starred = None, overrideFile=False):
    
    return self._resourcesManager._upload(self._id, name, file, description, mimeType, thumbnail, thumbnailMimeType, starred, overrideFile)

  def createFolder(self, name, description):
    
    return self._resourcesManager._createFolder(self._id, name, description)

  def delete(self):
    return self._resourcesManager._delete(self._id);
