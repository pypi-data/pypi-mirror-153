"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from .epmdataobject import EpmDataObject
from .itempathjson import ItemPathJSON
from .epmproperty import EpmProperty
from .epmnodeids import EpmNodeIds

import collections


class EpmObject(object):
    """description of class"""

    def __init__(self, epmConnection, itemPath, path, name, type = ''):
        self._epmConnection = epmConnection
        self._itemPath = itemPath
        self._path = path
        self._type = type
        self._name = name

    # Public Methods
    def enumObjects(self):
        childObjects = collections.OrderedDict()
        result = self._epmConnection._browse([self._itemPath], EpmNodeIds.HasComponent.value).references()[0]
        if len(result) < 1:
            return childObjects
        
        identities = [ItemPathJSON('OPCUA.NodeId', '', item._identity) for item in result]
        typesResults = self._epmConnection._browse(identities, EpmNodeIds.HasTypeDefinition.value).references()

        for index in range(0, len(result)):
            if result[index]._nodeClass == 4:  # Method is ignored
                continue
            childObjects[result[index]._displayName] = EpmObject(self._epmConnection, identities[index],
                                                        self._path + '/' + result[index]._displayName, result[index]._displayName,
                                                        typesResults[index][0]._displayName)

        return childObjects

    def enumProperties(self):
      result = self._epmConnection._browse([ self._itemPath ], EpmNodeIds.HasProperty.value)
      childProperties = collections.OrderedDict()
      for item in result.references()[0]:
        childProperties[item._displayName] = EpmProperty(self._epmConnection, item._displayName, self._path + '/' + item._displayName, ItemPathJSON('OPCUA.NodeId', '', item._identity))
      return childProperties

    # Public Properties

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

