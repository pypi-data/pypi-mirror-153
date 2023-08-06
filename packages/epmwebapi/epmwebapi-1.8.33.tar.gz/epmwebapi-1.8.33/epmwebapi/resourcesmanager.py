"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

import requests
import json
import collections

from .folder import Folder
from .resource import Resource
from .downloadtype import DownloadType

from .mimetype import Application, Text, Image, Audio, Video

class ResourcesManager(object):

  def __init__(self, authorizationService, webApi, baseFolderId):
    self._authorizationService = authorizationService
    self._webApi = webApi
    self._baseFolderId = baseFolderId

  def browse(self):
    return self._browse(self._baseFolderId)

  def getResource(self, path):
    return self._getResource(self._baseFolderId + (('/' + path) if len(path) > 0 else ''))

  def createFolder(self, name, description=None):
    return self._createFolder(self._baseFolderId, name, description)

  def _getResource(self, path = None, id = None):

    odata = ""
    if path != None:
      odata = "files('path:" + path + "')"
    elif id != None:
      odata = "files('" + id + "')"

    url = self._webApi + "/resource/odata/v2/" + odata

    session = self._authorizationService.getSession()
    response = session.get(url, verify=False)
    if response.status_code != 200:
        print(response.reason)
        raise Exception("Browse service call http error '" +  str(response.status_code) + "'. Reason: " + response.reason)

    json_result = json.loads(response.text)
    if json_result == None:
      raise Exception("Read Failed no result")

    if json_result['mimeType'] == Application.ElipsePortalFolder.value:
      return Folder(self, json_result['identity'], json_result['name'], json_result['description'])
    else:
      return Resource(self, json_result['identity'], json_result['name'], json_result['description'], json_result['mimeType'])

  def _browse(self, folderId):

    url = self._webApi + "/resource/odata/v2/files('" + folderId + "')/children(recursive=false)?$format=application/json;odata.metadata=none"

    session = self._authorizationService.getSession()
    response = session.get(url, verify=False)
    if response.status_code != 200:
        print(response.reason)
        raise Exception("Browse service call http error '" +  str(response.status_code) + "'. Reason: " + response.reason)

    json_result = json.loads(response.text)
    if json_result == None:
        raise Exception("Read Failed no result")

    children = collections.OrderedDict()
    for item in json_result['value']:
      if item['mimeType'] == Application.ElipsePortalFolder.value:
        children[item['name']] = Folder(self, item['identity'], item['name'], item['description'])
      else:
        children[item['name']] = Resource(self, item['identity'], item['name'], item['description'], item['mimeType'])

    return children

  def _download(self, resourceId, type):

    import urllib
    from urllib.request import urlopen, Request
    import io
    from shutil import copyfileobj

    if isinstance(type, DownloadType):
      typeName = type.value
    else:
      typeName = type

    resourceId = urllib.parse.quote(resourceId, safe='')

    token = self._authorizationService.getToken()
    url = self._webApi + "/resource/v2/files/" + resourceId
    header = {'Authorization': 'Bearer {}'.format(token)}

    request = Request(url, headers=header)

    chunk_size = 8096
    with urlopen(request) as response:
      if typeName == DownloadType.Binary.value:
        resourceStream = io.BytesIO()
        copyfileobj(response, resourceStream, chunk_size)
        resourceStream.seek(0)
        return resourceStream
      elif typeName == DownloadType.Text.value:
        return response.read().decode('utf-8')
      elif typeName == DownloadType.Json.value:
        return json.loads(response.read())
      else:
        raise Exception("Invalid download file type '" +  str(response.status_code) + "'. Reason: " + response.reason)

  def _upload(self, parentId, name, file, description = None, mimeType = None, thumbnail = None, thumbnailMimeType = None, starred = None, overrideFile = False):

    if isinstance(mimeType, Application) | isinstance(mimeType, Text) | isinstance(mimeType, Image) | isinstance(mimeType, Audio) | isinstance(mimeType, Video):
      mimeTypeName = mimeType.value
    else:
      mimeTypeName = mimeType


    from requests_toolbelt.multipart.encoder import MultipartEncoder

    metadata = { 'name': name,
                 'description': description,
                 'mimeType': mimeTypeName,
                 'thumbnail': thumbnail,
                 'thumbnailMimeType': thumbnailMimeType,
                 'parents': [ parentId],
                 'starred': starred }

    m = MultipartEncoder(fields={'__metadata': ( "blob", json.dumps(metadata), "application/json"), 
                                 'file': (name, file, mimeTypeName)})

    token = self._authorizationService.getToken()
    url = self._webApi + "/resource/v2/upload/files"
    header = {'Content-Type': m.content_type, 'Authorization': 'Bearer {}'.format(token)}

    session = self._authorizationService.getSession()
    response = session.post(url, headers=header, data=m, verify=False)

    if response.status_code == 409 and overrideFile:
      exitentResource = self._browse(parentId)[name]
      file.seek(0)
      self._updateFile(exitentResource._id, exitentResource._name, exitentResource._mimeType, file)
      return exitentResource

    elif response.status_code != 200:
      print(response.reason)
      raise Exception("Upload call http error '" +  str(response.status_code) + "'. Reason: " + response.reason)

    json_result = json.loads(response.text)

    resource =  Resource(self, json_result['items'][0]['identity'], json_result['items'][0]['name'], json_result['items'][0]['description'], json_result['items'][0]['mimeType'])

    return resource

  def _createFolder(self, parentId, name, description):

    from requests_toolbelt.multipart.encoder import MultipartEncoder

    metadata = { 'name': name,
                 'description': description,
                 'mimeType': 'application/vnd.elipse.portal.folder',
                 'thumbnail': None,
                 'thumbnailMimeType': None,
                 'parents': [ parentId ],
                 'starred': None }

    m = MultipartEncoder(fields={'__metadata': ( "blob", json.dumps(metadata), "application/json")})

    token = self._authorizationService.getToken()
    url = self._webApi + "/resource/v2/upload/files"
    header = {'Content-Type': m.content_type, 'Authorization': 'Bearer {}'.format(token)}

    session = self._authorizationService.getSession()
    response = session.post(url, headers=header, data=m, verify=False)

    if response.status_code != 200:
      print(response.reason)
      raise Exception("CreateFolder call http error '" +  str(response.status_code) + "'. Reason: " + response.reason)
    json_result = json.loads(response.text)

    folder = Folder(self, json_result['items'][0]['identity'], json_result['items'][0]['name'], json_result['items'][0]['description'])

    return folder

  def _updateFile(self, id, name, mimeType, file):

    from requests_toolbelt.multipart.encoder import MultipartEncoder
    import urllib

    metadata = { 'name': name,
                 #'description': description,
                 'mimeType': mimeType }
                 #'thumbnail': thumbnail,
                 #'thumbnailMimeType': thumbnailMimeType,
                 #'parents': [ parentId],
                 #'starred': starred }

    m = MultipartEncoder(fields={'__metadata': ( "blob", json.dumps(metadata), "application/json"), 
                                 'file': (name, file, mimeType)})

    id = urllib.parse.quote(id, safe='')

    token = self._authorizationService.getToken()
    url = self._webApi + "/resource/v2/files/" + id
    header = {'Content-Type': m.content_type, 'Authorization': 'Bearer {}'.format(token)}

    session = self._authorizationService.getSession()
    response = session.patch(url, headers=header, data=m, verify=False)

    if response.status_code != 200:
      print(response.reason)
      raise Exception("Upload call http error '" +  str(response.status_code) + "'. Reason: " + response.reason)

  def _delete(self, id):

    url = self._webApi + "/resource/odata/v2/files('" + id + "')"

    session = self._authorizationService.getSession()
    response = session.delete(url, verify=False)
    if response.status_code != 200:
        print(response.reason)
        raise Exception("Delete service call http error '" +  str(response.status_code) + "'. Reason: " + response.reason)

